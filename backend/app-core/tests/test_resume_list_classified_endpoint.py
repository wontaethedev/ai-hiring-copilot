import pytest
import httpx
from unittest.mock import patch, AsyncMock
from fastapi import status
from app import app
from sqlalchemy.ext.asyncio import AsyncSession
from lib.models.resume import ListClassifiedResponse, ResumeDetails

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
async def test_list_classified_success(client, mock_db_session):
    # Mock processed resumes returned from DB
    mock_resumes = [
        AsyncMock(id="1", base_requirement_satisfaction_score=85, exceptional_considerations="Great fit", fitness_score=80),
        AsyncMock(id="2", base_requirement_satisfaction_score=60, exceptional_considerations="Good fit", fitness_score=45),
        AsyncMock(id="3", base_requirement_satisfaction_score=30, exceptional_considerations="Needs improvement", fitness_score=20),
    ]
    
    with patch("router.resume.ResumeDBHelper.select_by_filters", return_value=mock_resumes):
        response = await client.get("/resume/list_classified")
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify response content
        response_data = ListClassifiedResponse(**response.json())
        
        assert len(response_data.very_fit) == 1  # Only one resume should be in `very_fit`
        assert response_data.very_fit[0] == ResumeDetails(
            id="1",
            base_requirement_satisfaction_score=85,
            exceptional_considerations="Great fit",
            fitness_score=80
        )
        
        assert len(response_data.fit) == 1  # Only one resume should be in `fit`
        assert response_data.fit[0] == ResumeDetails(
            id="2",
            base_requirement_satisfaction_score=60,
            exceptional_considerations="Good fit",
            fitness_score=45
        )
        
        assert len(response_data.not_fit) == 1  # Only one resume should be in `not_fit`
        assert response_data.not_fit[0] == ResumeDetails(
            id="3",
            base_requirement_satisfaction_score=30,
            exceptional_considerations="Needs improvement",
            fitness_score=20
        )

@pytest.mark.asyncio
async def test_list_classified_incomplete_resumes(client, mock_db_session):
    # Mock resumes with missing fields
    mock_resumes = [
        AsyncMock(id="1", base_requirement_satisfaction_score=None, exceptional_considerations="Incomplete", fitness_score=None),
        AsyncMock(id="2", base_requirement_satisfaction_score=60, exceptional_considerations=None, fitness_score=45),
    ]
    
    with patch("router.resume.ResumeDBHelper.select_by_filters", return_value=mock_resumes):
        response = await client.get("/resume/list_classified")
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify no resumes classified due to missing fields
        response_data = ListClassifiedResponse(**response.json())
        
        assert len(response_data.very_fit) == 0
        assert len(response_data.fit) == 0
        assert len(response_data.not_fit) == 0

@pytest.mark.asyncio
async def test_list_classified_database_error(client, mock_db_session):
    # Mock database error in select_by_filters
    with patch("router.resume.ResumeDBHelper.select_by_filters", side_effect=Exception("Database error")):
        response = await client.get("/resume/list_classified")
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Failed to fetch processed resumes from DB" in response.json()["detail"]

@pytest.mark.asyncio
async def test_list_classified_processing_error(client, mock_db_session):
    # Mock valid resumes, but induce error during classification
    mock_resumes = [
        AsyncMock(id="1", base_requirement_satisfaction_score=85, exceptional_considerations="Great fit", fitness_score=None),
    ]
    
    with patch("router.resume.ResumeDBHelper.select_by_filters", return_value=mock_resumes):
        response = await client.get("/resume/list_classified")
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify that no resumes are classified due to the error during processing
        response_data = ListClassifiedResponse(**response.json())
        
        assert len(response_data.very_fit) == 0
        assert len(response_data.fit) == 0
        assert len(response_data.not_fit) == 0
