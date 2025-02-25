from pydantic import BaseModel

class HealthRequest(BaseModel):
    message: str | None = None


class HealthResponse(BaseModel):
    healthy: bool
    message: str | None = None


class DbInsertRequest(BaseModel):
    message: str
    number: int


class DBInsertResponse(BaseModel):
    success: bool
    id: str
    message: str
    number: int
