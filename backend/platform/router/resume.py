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
)
from sqlalchemy.ext.asyncio import AsyncSession

from lib.models.product.resume import RoleTypes, StatusTypes
from lib.models.resume import (
  RegisterResponse,
  ResumeDetails,
  ListClassifiedResponse,
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
  files: list[UploadFile] = File(...),
  db: AsyncSession = Depends(get_db),
) -> RegisterResponse:
  processed_resume_ids: list[str] = []

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
        resume_text = extract_text_from_pdf(tmp_file_path)
      elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text = extract_text_from_word(tmp_file_path)
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


@router.get("/list_classified")
async def list_classified(
  db: AsyncSession = Depends(get_db),
) -> ListClassifiedResponse:
  very_fit_resumes: list[ResumeDetails] = []
  fit_resumes: list[ResumeDetails] = []
  not_fit_resumes: list[ResumeDetails] = []

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

        # Classify resume depending on fitness score
        curr_resume: ResumeDetails = ResumeDetails(
          id=resume_id,
          base_requirement_satisfaction_score=resume_base_requirement_satisfaction_score,
          exceptional_considerations=resume_exceptional_considerations,
          fitness_score=resume_fitness_score,
        )
        if resume_fitness_score >= 75:
          very_fit_resumes.append(curr_resume)
        elif resume_fitness_score >= 40:
          fit_resumes.append(curr_resume)
        else:
          not_fit_resumes.append(curr_resume)
      except Exception as e:
        # Do nothing, move on to next resume
        logging.error(f"Failed to parse resume details | {str(e)}")
  except Exception as e:
    # Should not happen
    raise HTTPException(status_code=500, detail=f"Failed to prepare processed resumes | {str(e)}")

  return ListClassifiedResponse(
    very_fit=very_fit_resumes,
    fit=fit_resumes,
    not_fit=not_fit_resumes,
  )
