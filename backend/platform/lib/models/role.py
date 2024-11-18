from pydantic import BaseModel


class RegisterResponse(BaseModel):
  id: str
