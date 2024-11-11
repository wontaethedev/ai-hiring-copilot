from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from lib.models.product.resume import RoleTypes, StatusTypes

from db.models import Resume


class ResumeDBHelper:
  async def select_by_filters(
    session: AsyncSession,
    status: StatusTypes,
    max_num_resumes: int,
  ) -> list[Resume]:
    stmt = select(Resume).where(Resume.status == status).limit(max_num_resumes)
    result = await session.execute(stmt)
    resumes = result.scalars().all()
    return resumes

  async def insert(
    session: AsyncSession,
    role: RoleTypes,
    status: StatusTypes,
    content: str,
  ) -> str:
    new_resume: Resume = Resume(
      role=role,
      status=status,
      content=content,
    )

    session.add(new_resume)
    await session.commit()
    await session.refresh(new_resume)

    return new_resume.id

  async def update(
    session: AsyncSession,
    id: str,
    base_requirement_satisfaction_score: int,
    exceptional_considerations: str,
    fitness_score: int,
  ):
    stmt = update(Resume).where(Resume.id == id).values(
      base_requirement_satisfaction_score=base_requirement_satisfaction_score,
      exceptional_considerations=exceptional_considerations,
      fitness_score=fitness_score,
    )
    await session.execute(stmt)
    await session.commit()

  async def update_status(
    session: AsyncSession,
    id: str,
    status: StatusTypes,
  ):
    stmt = update(Resume).where(Resume.id == id).values(
      status=status,
    )
    await session.execute(stmt)
    await session.commit()
