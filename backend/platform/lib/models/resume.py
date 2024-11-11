from pydantic import BaseModel


class RegisterResponse(BaseModel):
    ids: list[str]
