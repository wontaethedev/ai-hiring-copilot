from pydantic import BaseModel


class RegisterResponse(BaseModel):
  ids: list[str]


class ResumeDetails(BaseModel):
  id: str
  base_requirement_satisfaction_score: int
  exceptional_considerations: str
  fitness_score: int
