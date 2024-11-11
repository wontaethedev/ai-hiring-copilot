import os
import logging
import tempfile

from fastapi import (
  APIRouter,
  File,
  UploadFile,
  HTTPException,
  Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from lib.models.product.resume import RoleTypes, StatusTypes
from lib.models.resume import (
  RegisterResponse,
  ResumeDetails,
)
from lib.helpers.pdf import (
   extract_text_from_pdf
)
from lib.helpers.db.resume import ResumeDBHelper
from lib.scripts.process_resumes import process_resumes

from db.db import get_db
from db.models import Resume


router = APIRouter()


@router.post("/register")
async def register(
  files: list[UploadFile] = File(...),
  db: AsyncSession = Depends(get_db),
) -> RegisterResponse:
  processed_resume_ids: list[str] = []

  # TODO: SECURITY - sanitization, file size check (unless enforced on nginx level), harmful content, etc.
  for file in files:
    if file.content_type != "application/pdf":
      raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")

    try:
      # Read file
      contents = await file.read()
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"Failed to read file | {str(e)}")

    try:
      # Save the uploaded file to a temporary file
      with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
          tmp_file.write(contents)
          tmp_file_path = tmp_file.name
      # Extract text from the PDF file
      resume_text = extract_text_from_pdf(tmp_file_path)
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"Failed to extract text from pdf | {str(e)}")
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
        role=RoleTypes.SENIOR_PRODUCT_ENGINEER,
        status=StatusTypes.PENDING,
        content=resume_text,
      )
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"Failed to save processed resumes into the DB | {str(e)}")
    try:
      processed_resume_ids.append(inserted_resume_id)
    except Exception as e:
      logging.error(f"Failed to parse ID from DB inserted resume | {str(e)}")

  return RegisterResponse(ids=processed_resume_ids)


@router.post("/process")
async def process():
  result = await process_resumes()
  return result


@router.get("/")
async def list_resumes(
  db: AsyncSession = Depends(get_db),
) -> list[ResumeDetails]:
  result: list[ResumeDetails] = []

  try:
    # Fetch processed resumes from the DB
    processed_resumes: list[Resume] = await ResumeDBHelper.select_by_filters(
      session=db,
      status=StatusTypes.COMPLETE,
      max_num_resumes=100,
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Failed to fetch processed resumes from DB | {str(e)}")

  try:
    # Loop over each resume, parse & validate details
    for resume in processed_resumes:
      try:
        # Parse resume details
        resume_id: str =  resume.id
        resume_base_requirement_satisfaction_score: int | None = resume.base_requirement_satisfaction_score
        resume_exceptional_considerations: str | None = resume.exceptional_considerations
        resume_fitness_score: int | None = resume.fitness_score

        # Validate resume details
        if (
          resume_base_requirement_satisfaction_score is None
          or resume_exceptional_considerations is None
          or resume_fitness_score is None
        ):
          raise Exception("Resume does not have necessary assessment details")

        # Resume has necessary details, append to result
        result.append(
          ResumeDetails(
            id=resume_id,
            base_requirement_satisfaction_score=resume_base_requirement_satisfaction_score,
            exceptional_considerations=resume_exceptional_considerations,
            fitness_score=resume_fitness_score,
          )
        )
      except Exception as e:
        # Do nothing, move on to next resume
        logging.error(f"Failed to parse resume details | {str(e)}")
  except Exception as e:
    # Should not happen
    raise HTTPException(status_code=500, detail=f"Failed to prepare processed resumes | {str(e)}")

  return result
