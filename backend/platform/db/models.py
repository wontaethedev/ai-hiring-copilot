from sqlalchemy import Column, Integer, String, Enum, Text
from sqlalchemy.orm import declarative_base

from lib.helpers.ulid import generate_ulid
from lib.models.product.resume import RoleTypes, StatusTypes


Base = declarative_base()


class Test(Base):
  __tablename__ = 'test'

  id: str = Column(String, primary_key=True, default=generate_ulid)
  message: str = Column(String)
  number: int = Column(Integer)


class Resume(Base):
  __tablename__ = 'resume'

  id: str = Column(String, primary_key=True, default=generate_ulid)
  role: str = Column(Enum(RoleTypes), nullable=False)
  status: str = Column(Enum(StatusTypes), nullable=False)
  content: str = Column(Text, nullable=False) # TODO: User input - sanitization, length limit, etc.

  base_requirement_satisfaction_score: int | None = Column(Integer)
  exceptional_considerations: str | None = Column(String)
  fitness_score: int | None = Column(Integer)
  # TODO: Add created_at
