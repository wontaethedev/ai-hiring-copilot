import logging

from lib.helpers.openai import OpenAIHelper
from lib.helpers.db.resume import ResumeDBHelper
from lib.helpers.db.role import RoleDBHelper
from lib.data.openai import OPEN_AI_API_KEY, OPEN_AI_ORGANIZATION_ID, TOOLS, SYSTEM_MSGS

from lib.models.product.resume import RoleTypes, StatusTypes

from db.db import get_context_managed_session
from db.models import Resume, Role

async def process_resumes(
) -> list[str]:
  """
  Processes resumes of status PENDING by using OpenAI for
  assessment based on preset data in `platform/lib/data/openai.py`.

  NOTE: Fill in `OPEN_AI_API_KEY` and `OPEN_AI_ORGANIZATION_ID` in the preset data file to use this script.
    TODO: move to config or .env

  TODO: Add `created_at` in `Resume` model and process from oldest resume
  TODO: Make `max_num_resumes` controllable

  Returns:
    - list[str]: The IDs of resumes that were processed
  """

  processed_resume_ids: list[str] = []

  async with get_context_managed_session() as session:
    resumes: list[Resume] = await ResumeDBHelper.select_by_filters(
      session=session,
      status=StatusTypes.PENDING,
    )

    resume_ids: list[str] = [resume.id for resume in resumes]

    try:
      await ResumeDBHelper.bulk_update_status(
        session=session,
        ids=resume_ids,
        status=StatusTypes.IN_PROGRESS
      )
    except Exception as e:
      await ResumeDBHelper.bulk_update_status(session=session, ids=resume_ids, status=StatusTypes.FAILED)
      raise Exception(f"Failed to set target resumes in status IN_PROGRESS | {str(e)}")


    for resume in resumes:
      resume_id: str = resume.id
      resume_content: str = resume.content
      resume_role_id: str = resume.role_id

      try:
        resume_role: Role = await RoleDBHelper.get_role(session=session, id=resume_role_id)
      except Exception as e:
        await ResumeDBHelper.update_status(session=session, id=resume_id, status=StatusTypes.FAILED)
        logging.error(f"Could not find associated role for the resume | {str(e)}")
        continue

      role_description: str = resume_role.description

      try:
        openai_helper: OpenAIHelper = OpenAIHelper(
          api_key=OPEN_AI_API_KEY,
          organization_id=OPEN_AI_ORGANIZATION_ID,
        )

        # Process resume through OpenAI
        resume_data = openai_helper.function_call_prompt(
          user_msg=f"Here is the resume text: {str(resume_content)}",
          system_msg=f"""
            You are a copilot assisting a hiring manager review resumes.
            Here is the job description:
            {role_description}
          """,
          tools=[TOOLS[RoleTypes.SENIOR_PRODUCT_ENGINEER]],
        )
      except Exception as e:
        await ResumeDBHelper.update_status(session=session, id=resume_id, status=StatusTypes.FAILED)
        logging.error(f"Failed to assess resume using OpenAI | {str(e)}")
        continue

      try:
        base_requirement_satisfaction_score: int = resume_data['base_requirement_satisfaction_score']
        exceptionals: str = resume_data['exceptionals']
        fitness_score: int = resume_data['fitness_score']
      except Exception as e:
        await ResumeDBHelper.update_status(session=session, id=resume_id, status=StatusTypes.FAILED)
        logging.error(f"Failed to parse assessment data from OpenAI response | {str(e)}")
        continue

      try:
        await ResumeDBHelper.update(
          session=session,
          id=resume_id,
          base_requirement_satisfaction_score=base_requirement_satisfaction_score,
          exceptional_considerations=exceptionals,
          fitness_score=fitness_score,
        )
      except Exception as e:
        await ResumeDBHelper.update_status(session=session, id=resume_id, status=StatusTypes.FAILED)
        logging.error(f"Failed to update resume information using OpenAI response | {str(e)}")
        continue

      try:
        await ResumeDBHelper.update_status(session=session, id=resume_id, status=StatusTypes.COMPLETE)
      except Exception as e:
        await ResumeDBHelper.update_status(session=session, id=resume_id, status=StatusTypes.FAILED)
        logging.error(f"Failed to update status of new resume to COMPLETE | {str(e)}")
        continue

      processed_resume_ids.append(resume_id)

    return processed_resume_ids
  