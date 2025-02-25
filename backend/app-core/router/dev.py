import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.models.dev import (
  HealthRequest,
  HealthResponse,
  DbInsertRequest,
  DBInsertResponse,
)
from db.db import get_db
from db.models import Test

router = APIRouter()

@router.post("/")
async def health(request: HealthRequest) -> HealthResponse:
  return HealthResponse(
      healthy=True,
      message=request.message
  )

@router.post("/db_insert")
async def db_insert(
  request: DbInsertRequest,
  db: AsyncSession = Depends(get_db),
) -> DBInsertResponse:
  message: str = request.message
  number: int = request.number

  new_test: Test = Test(
    message=message,
    number=number,
  )
  db.add(new_test)
  await db.commit()
  await db.refresh(new_test)

  return DBInsertResponse(
    success=True,
    id=new_test.id,
    message=new_test.message,
    number=new_test.number,
  )
