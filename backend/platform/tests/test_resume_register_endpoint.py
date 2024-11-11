import pytest
import httpx
from unittest.mock import patch, ANY
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from app import app
from lib.models.product.resume import RoleTypes, StatusTypes

@pytest.fixture
def client():
    from httpx import ASGITransport
    transport = ASGITransport(app=app)
    return httpx.AsyncClient(transport=transport, base_url="http://test")

@pytest.fixture
async def mock_db_session():
    async with AsyncSession() as session:
        yield session

@pytest.mark.asyncio
async def test_register_pdf_file_success(client, mock_db_session):
    with patch("router.resume.extract_text_from_pdf", return_value="Extracted PDF text"):
        with patch("router.resume.ResumeDBHelper.insert", return_value="mock_resume_id") as mock_insert:
            files = [("files", ("resume.pdf", b"PDF file content", "application/pdf"))]
            response = await client.post("/resume/register", files=files)

            assert response.status_code == status.HTTP_200_OK
            assert response.json()["ids"] == ["mock_resume_id"]

            mock_insert.assert_called_once_with(
                session=ANY,
                role=RoleTypes.SENIOR_PRODUCT_ENGINEER,
                status=StatusTypes.PENDING,
                content="Extracted PDF text",
            )

@pytest.mark.asyncio
async def test_register_docx_file_success(client, mock_db_session):
    with patch("router.resume.extract_text_from_word", return_value="Extracted DOCX text"):
        with patch("router.resume.ResumeDBHelper.insert", return_value="mock_resume_id") as mock_insert:
            files = [("files", ("resume.docx", b"DOCX file content", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))]
            response = await client.post("/resume/register", files=files)

            assert response.status_code == status.HTTP_200_OK
            assert response.json()["ids"] == ["mock_resume_id"]

            mock_insert.assert_called_once_with(
                session=ANY,
                role=RoleTypes.SENIOR_PRODUCT_ENGINEER,
                status=StatusTypes.PENDING,
                content="Extracted DOCX text",
            )

@pytest.mark.asyncio
async def test_register_invalid_file_type(client, mock_db_session):
    # Test for an unsupported file type
    files = [("files", ("resume.txt", b"Invalid file content", "text/plain"))]
    response = await client.post("/resume/register", files=files)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Invalid file type. Please upload a PDF of DOCX file."

@pytest.mark.asyncio
async def test_register_missing_file(client, mock_db_session):
    # Test for missing files
    response = await client.post("/resume/register", files=[])
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # FastAPI raises 422 for missing required fields

@pytest.mark.asyncio
async def test_register_large_file(client, mock_db_session):
    # Simulate a very large file
    large_content = b"a" * 10**7  # 10 MB content
    files = [("files", ("large_resume.pdf", large_content, "application/pdf"))]

    with patch("router.resume.extract_text_from_pdf", return_value="Extracted PDF text"):
        with patch("router.resume.ResumeDBHelper.insert", return_value="mock_resume_id"):
            response = await client.post("/resume/register", files=files)
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["ids"] == ["mock_resume_id"]

@pytest.mark.asyncio
async def test_register_pdf_parsing_error(client, mock_db_session):
    # Test for a file parsing error in PDF
    with patch("router.resume.extract_text_from_pdf", side_effect=Exception("PDF parsing error")):
        files = [("files", ("resume.pdf", b"PDF content", "application/pdf"))]
        response = await client.post("/resume/register", files=files)
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Failed to extract text from provided file" in response.json()["detail"]

@pytest.mark.asyncio
async def test_register_docx_parsing_error(client, mock_db_session):
    # Test for a file parsing error in DOCX
    with patch("router.resume.extract_text_from_word", side_effect=Exception("DOCX parsing error")):
        files = [("files", ("resume.docx", b"DOCX content", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))]
        response = await client.post("/resume/register", files=files)
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Failed to extract text from provided file" in response.json()["detail"]

@pytest.mark.asyncio
async def test_register_db_insert_error(client, mock_db_session):
    # Test for database insertion error
    with patch("router.resume.extract_text_from_pdf", return_value="Extracted PDF text"):
        with patch("router.resume.ResumeDBHelper.insert", side_effect=Exception("Database insert error")):
            files = [("files", ("resume.pdf", b"PDF content", "application/pdf"))]
            response = await client.post("/resume/register", files=files)
            
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "Failed to save processed resumes into the DB" in response.json()["detail"]
