from sqlalchemy import Column, Integer, String

from db.db import Base
from lib.helpers.ulid import generate_ulid


class Test(Base):
  __tablename__ = 'test'

  id: str = Column(String, primary_key=True, default=generate_ulid)
  message: str = Column(String)
  number: int = Column(Integer)
