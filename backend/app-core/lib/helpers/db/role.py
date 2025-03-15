# from sqlalchemy import select, update
# from sqlalchemy.ext.asyncio import AsyncSession

# from db.models import Role


# class RoleDBHelper:
#   async def get_role(
#     session: AsyncSession,
#     id: str,
#   ) -> Role:
#     """
#     Fetch a role from the DB by ID.

#     Returns:
#       - The role with matching ID
#     """

#     stmt = select(Role).where(Role.id == id)
#     result = await session.execute(stmt)
#     role = result.scalars().first()

#     if not role:
#       raise ValueError(f"Role with ID {id} not found.")

#     return role


#   async def list_roles(
#     session: AsyncSession,
#   ) -> list[Role]:
#     """
#     Lists all roles from the DB.
#     TODO: Add constraint to num roles

#     Returns:
#       - A list of all roles
#     """

#     stmt = select(Role)
#     result = await session.execute(stmt)
#     roles = result.scalars().all()
#     return roles

#   async def insert(
#     session: AsyncSession,
#     name: str,
#     description: str,
#   ) -> str:
#     """
#     Inserts a role into the DB

#     Args:
#       - The description of the role.
#         NOTE: Should be parsed from markdown.

#     Returns:
#       - The ID of the inserted role
#     """

#     new_role: Role = Role(
#       name=name,
#       description=description
#     )

#     session.add(new_role)
#     await session.commit()
#     await session.refresh(new_role)

#     return new_role.id

#   async def update(
#     session: AsyncSession,
#     id: str,
#     name: str,
#     description: str,
#   ) -> None:
#     """
#     Update a role in the DB.

#     Args:
#       - id: The ID of the role to update
#       - description: The new description of the role
#     """

#     stmt = update(Role).where(Role.id == id).values(
#       name=name,
#       description=description,
#     )
#     await session.execute(stmt)
#     await session.commit()
