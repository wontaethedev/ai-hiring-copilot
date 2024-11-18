from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from lib.models.product.resume import StatusTypes, ClassifierTypes

from db.models import Resume


class ResumeDBHelper:
  async def select_by_filters(
    session: AsyncSession,
    role_id: str,
    status: StatusTypes = None,
    classifier: ClassifierTypes = None,
  ) -> list[Resume]:
    """
    Retrieves resume details by given filters from the DB.
    """

    stmt = select(Resume).where(Resume.role_id == role_id)

    if status:
      stmt.where(Resume.status == status)
    
    if classifier:
      if classifier == ClassifierTypes.VERY_FIT:
        stmt.where(Resume.fitness_score >= 85)
      elif classifier == ClassifierTypes.FIT:
        stmt = stmt.where(Resume.fitness_score < 85)
        stmt = stmt.where(Resume.fitness_score >= 50)
      elif classifier == ClassifierTypes.UNFIT:
        stmt = stmt.where(Resume.fitness_score < 50)
      else:
        # Should not happen
        # TODO: Raise exception
        pass

    result = await session.execute(stmt)
    resumes = result.scalars().all()
    return resumes

  async def insert(
    session: AsyncSession,
    role_id: str,
    status: StatusTypes,
    content: str,
  ) -> str:
    """
    Inserts resume details into the DB
    """

    new_resume: Resume = Resume(
      role_id=role_id,
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
  ) -> None:
    """
    Update resume details in the DB.
    TODO: Helper function should be more robust instead of for specific use-case.
    """

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
  ) -> None:
    """
    Updates the status of a resume detail in the DB.
    """
    stmt = update(Resume).where(Resume.id == id).values(
      status=status,
    )
    await session.execute(stmt)
    await session.commit()
  
  async def bulk_update_status(
    session: AsyncSession,
    ids: list[str],
    status: StatusTypes,
  ) -> None:
    """
    Updates the status of resume details in bulk.
    """
    stmt = (
      update(Resume)
      .where(Resume.id.in_(ids))
      .values(status=status)
    )
    await session.execute(stmt)
    await session.commit() 
