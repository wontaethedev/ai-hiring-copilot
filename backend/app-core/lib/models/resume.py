from pydantic import BaseModel


class RegisterResponse(BaseModel):
  ids: list[str]


class ResumeDetails(BaseModel):
  """
  base_requirement_satisfaction_score: How much the candidate satisfies the base requirements out of 100.
  exceptional_considerations: Any exceptional stand outs that may put the candidate for particular consideration.
  fitness_score: How fit the candidate is for the role out of 100.
  """

  id: str
  base_requirement_satisfaction_score: int
  exceptional_considerations: str
  fitness_score: int


class ListClassifiedResponse(BaseModel):
  """
  very_fit: Fitness score >= 75, candidate is very fit for the role
  fit: 75 > Fitness score >= 40, candidate is fit for the role
  not_fit: 40 > Fitness score, candidate is not the most fit for the role
  """

  very_fit: list[ResumeDetails]
  fit: list[ResumeDetails]
  not_fit: list[ResumeDetails]
