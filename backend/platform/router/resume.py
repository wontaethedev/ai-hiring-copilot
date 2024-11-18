import os
import logging
import tempfile
from pathlib import Path

from fastapi import (
  APIRouter,
  File,
  UploadFile,
  HTTPException,
  Depends,
  Form,
)
from sqlalchemy.ext.asyncio import AsyncSession

from lib.models.product.resume import StatusTypes, ClassifierTypes
from lib.models.resume import (
  RegisterResponse,
  ResumeDetails,
)
from lib.helpers.pdf import (
   extract_text_from_pdf
)
from lib.helpers.worddoc import (
  extract_text_from_word
)
from lib.helpers.db.resume import ResumeDBHelper
from lib.scripts.process_resumes import process_resumes

from db.db import get_db
from db.models import Resume


router = APIRouter()


@router.post("/register")
async def register(
  role_id: str = Form(...),
  files: list[UploadFile] = File(...),
  db: AsyncSession = Depends(get_db),
) -> RegisterResponse:
  """
  Registers resume files into the DB into PENDING mode, for the given role.

  Registered resume files should be picked up by the script `lib/scripts/process_resumes.py` and processed
  according to the description of the role specified.

  Args:
    - role_id: The ID of the role that the resume files are for
    - files: The resume files to register into the DB
  Returns:
    - RegisterResponse: The ids of the resumes uploaded to the DB
  """

  registered_resume_ids: list[str] = []

  # TODO: SECURITY - sanitization, file size check (unless enforced on nginx level), harmful content, etc.
  for file in files:
    if file.content_type not in [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]:
      raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF of DOCX file.")

    try:
      # Read file
      contents = await file.read()
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"Failed to read file | {str(e)}")

    try:
      # Save the uploaded file to a temporary file
      file_extension = Path(file.filename).suffix
      with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
          tmp_file.write(contents)
          tmp_file_path = tmp_file.name

      # Extract text based on file type
      if file.content_type == "application/pdf":
        resume_text: str = extract_text_from_pdf(tmp_file_path)
      elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text: str = extract_text_from_word(tmp_file_path)
      else:
        raise Exception("Failed to recognize content type of file.")
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"Failed to extract text from provided file | {str(e)}")
    finally:
      # Delete the temporary file if it exists
      if tmp_file_path and os.path.exists(tmp_file_path):
          try:
            os.unlink(tmp_file_path)
          except Exception as e:
            # Not mission critical, log error and continue
            logging.error(f"Failed to delete temporary file | {str(e)}")

    try:
      # Insert resume into DB in pending status
      inserted_resume_id: str = await ResumeDBHelper.insert(
        session=db,
        role_id=role_id,
        status=StatusTypes.PENDING,
        content=resume_text,
      )
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"Failed to save processed resumes into the DB | {str(e)}")
    try:
      registered_resume_ids.append(inserted_resume_id)
    except Exception as e:
      logging.error(f"Failed to parse ID from DB inserted resume | {str(e)}")

  return RegisterResponse(ids=registered_resume_ids)


@router.post("/process")
async def process() -> list[str]:
  """
  Triggers the `process_resumes` script.
  This endpoint is strictly for testing purposes, and should be disabled in staging/prod environments
  TODO: Disable in development mode (ie: IS_DEV flag)

  The `process_resumes` script processes 5 pending resumes using OpenAI

  Returns:
    - list[str]: The IDs of resumes that were processed using the `process_resumes` script
  """

  try:
      result: list[str] = await process_resumes()
      return result
  except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))


@router.get("/list_by_filters")
async def list_by_filters(
  role_id: str,
  status: StatusTypes = None,
  classifier: ClassifierTypes = None,
  db: AsyncSession = Depends(get_db),
) -> list[ResumeDetails]:
  """
  Lists resumes by given filters.

  NOTE: Optional filters that are not provided are ignored.

  TODO: Security - limit max num of resumes returned

  Args:
    - role_id: The role that the resumes are for
    - status: The status to filter resumes by
    - The minimum fitness score to filter resumes by

  Returns:
    - list[ResumeDetails]: The list of resume details requested
  """

  try:
    # Fetch resumes from the DB
    resumes: list[Resume] = await ResumeDBHelper.select_by_filters(
      session=db,
      role_id=role_id,
      status=status,
      classifier=classifier,
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Failed to fetch resumes from DB | {str(e)}")

  try:
    resume_details: list[ResumeDetails] = [
      ResumeDetails(
        id=resume.id,
        base_requirement_satisfaction_score=resume.base_requirement_satisfaction_score,
        exceptional_considerations=resume.exceptional_considerations,
        fitness_score=resume.fitness_score
      )
      for resume in resumes
    ]
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Failed to process resumes fetched from DB | {str(e)}")

  return resume_details
