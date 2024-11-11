from sqlalchemy.ext.asyncio import AsyncSession

from lib.models.product.resume import RoleTypes, StatusTypes

from db.models import Resume


class ResumeDBHelper:
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