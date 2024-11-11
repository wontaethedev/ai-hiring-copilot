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
)
from lib.helpers.pdf import (
   extract_text_from_pdf
)
from lib.helpers.db.resume import ResumeDBHelper

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
