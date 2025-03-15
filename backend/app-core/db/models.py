from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from lib.helpers.ulid import generate_ulid


Base = declarative_base()


class Test(Base):
    __tablename__ = "test"

    id: str = Column(String, primary_key=True, default=generate_ulid)
    message: str = Column(String)
    number: int = Column(Integer)
