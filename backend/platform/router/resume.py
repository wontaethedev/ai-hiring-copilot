import os
import logging
import tempfile
from fastapi import (
  APIRouter,
  File,
  UploadFile,
  HTTPException,
)
from lib.models.resume import (
  RegisterResponse,
)
from lib.helpers.pdf import (
   extract_text_from_pdf
)


router = APIRouter()


@router.post("/register")
async def register(
  files: list[UploadFile] = File(...)
) -> RegisterResponse:
  processed_resume_ids: list[str] = []

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
      # Append metadata to response
      processed_resume_ids.append(resume_text)
    except:
      raise HTTPException(status_code=500, detail=f"Failed to extract text from pdf | {str(e)}")
    finally:
      # Delete the temporary file if it exists
      if tmp_file_path and os.path.exists(tmp_file_path):
          try:
            os.unlink(tmp_file_path)
          except:
            # Not mission critical, log error and continue
            logging.error("Failed to delete temporary file")

  return RegisterResponse(ids=processed_resume_ids)
