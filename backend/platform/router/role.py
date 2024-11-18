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

from lib.models.role import (
  RegisterResponse,
)
from lib.helpers.markdown import (
   extract_text_from_markdown
)
from lib.helpers.db.role import RoleDBHelper

from db.db import get_db

router = APIRouter()


@router.post("/register")
async def register(
  file: UploadFile = File(...),
  db: AsyncSession = Depends(get_db),
) -> RegisterResponse:
  """
  Registers a role into the DB.

  Args:
    - file: The job description for the role
  Returns:
    - RegisterResponse: The ID of the role uploaded to the DB
  """

  # TODO: SECURITY - sanitization, file size check (unless enforced on nginx level), harmful content, etc.
  if file.content_type not in [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "text/markdown",
      "text/x-markdown",
  ]:
    raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF, DOCX, or Markdown file.")

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
    
    # Extract text from markdown
    role_description: str = extract_text_from_markdown(tmp_file_path)
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
    # Insert role into DB
    registered_role_id: str = await RoleDBHelper.insert(
       session=db,
       description=role_description
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Failed to save role into the DB | {str(e)}")
  
  return RegisterResponse(id=registered_role_id)
