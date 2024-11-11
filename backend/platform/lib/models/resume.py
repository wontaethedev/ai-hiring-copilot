from pydantic import BaseModel


class RegisterResponse(BaseModel):
  ids: list[str]


class ResumeDetails(BaseModel):
  id: str
  base_requirement_satisfaction_score: int
  exceptional_considerations: str
  fitness_score: int


class ListClassifiedResponse(BaseModel):
  very_fit: list[ResumeDetails]
  fit: list[ResumeDetails]
  not_fit: list[ResumeDetails]
