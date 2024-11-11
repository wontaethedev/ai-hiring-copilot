from lib.helpers.openai import OpenAIHelper
from lib.data.openai import OPEN_AI_API_KEY, OPEN_AI_ORGANIZATION_ID, TOOLS, SYSTEM_MSGS

from lib.models.product.resume import RoleTypes

async def process_resumes() -> list[str]:
  openai_helper: OpenAIHelper = OpenAIHelper(
    api_key=OPEN_AI_API_KEY,
    organization_id=OPEN_AI_ORGANIZATION_ID,
  )

  # Process resume through OpenAI
  resume_data = openai_helper.function_call_prompt(
    user_msg="",
    system_msg=SYSTEM_MSGS[RoleTypes.SENIOR_PRODUCT_ENGINEER],
    tools=[TOOLS[RoleTypes.SENIOR_PRODUCT_ENGINEER]],
  )

  return resume_data
