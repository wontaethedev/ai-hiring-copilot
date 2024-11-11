from lib.helpers.openai import OpenAIHelper
from lib.helpers.db.resume import ResumeDBHelper
from lib.data.openai import OPEN_AI_API_KEY, OPEN_AI_ORGANIZATION_ID, TOOLS, SYSTEM_MSGS

from lib.models.product.resume import RoleTypes, StatusTypes

from db.db import get_context_managed_session
from db.models import Resume

async def process_resumes(
) -> list[str]:
  """
  TODO: Add created_at in Resume model and process from oldest resume
  TODO: Make max_num_resumes controllable
  """
  processed_resume_ids: list[str] = []

  async with get_context_managed_session() as session:
    resumes: list[Resume] = await ResumeDBHelper.select_by_filters(
      session=session,
      status=StatusTypes.PENDING,
      max_num_resumes=5,
    )

    for resume in resumes:
      resume_id: str = resume.id
      resume_content: str = resume.content

      try:
        openai_helper: OpenAIHelper = OpenAIHelper(
          api_key=OPEN_AI_API_KEY,
          organization_id=OPEN_AI_ORGANIZATION_ID,
        )

        # Process resume through OpenAI
        resume_data = openai_helper.function_call_prompt(
          user_msg=f"Here is the resume text: {str(resume_content)}",
          system_msg=SYSTEM_MSGS[RoleTypes.SENIOR_PRODUCT_ENGINEER],
          tools=[TOOLS[RoleTypes.SENIOR_PRODUCT_ENGINEER]],
        )
      except Exception as e:
        await ResumeDBHelper.update_status(session=session, id=resume_id, status=StatusTypes.FAILED)
        raise Exception(f"Failed to assess resume using OpenAI | {str(e)}")
      
      try:
        base_requirement_satisfaction_score: int = resume_data['base_requirement_satisfaction_score']
        exceptionals: str = resume_data['exceptionals']
        fitness_score: int = resume_data['fitness_score']
      except Exception as e:
        await ResumeDBHelper.update_status(session=session, id=resume_id, status=StatusTypes.FAILED)
        raise Exception(f"Failed to parse assessment data from OpenAI response | {str(e)}")

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
        raise Exception(f"Failed to update resume information using OpenAI response | {str(e)}")

      try:
        await ResumeDBHelper.update_status(session=session, id=resume_id, status=StatusTypes.COMPLETE)
      except Exception as e:
        await ResumeDBHelper.update_status(session=session, id=resume_id, status=StatusTypes.FAILED)
        raise Exception(f"Failed to update status of new resume to COMPLETE | {str(e)}")

      processed_resume_ids.append(resume_id)

    return processed_resume_ids
