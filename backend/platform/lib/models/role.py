from pydantic import BaseModel


class RoleDetails(BaseModel):
  id: str
  name: str
  description: str

class RegisterResponse(BaseModel):
  id: str
