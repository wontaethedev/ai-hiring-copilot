from openai import OpenAI
import json

class OpenAIHelper:
  def __init__(
    self,
    api_key: str,
    organization_id: str,
  ):
    self.client = OpenAI(
      api_key=api_key,
      organization=organization_id,
    )

  def function_call_prompt(
    self,
    user_msg: str,
    system_msg: str,
    tools: list[dict[str]],
  ):
    """
    Sends a function call prompt to OpenAPI
    """

    try:
      # Send function call prompt to OpenAPI
      response = self.client.chat.completions.create(
        model="gpt-4o-mini", # TODO: Make configurable
        messages=[
          {"role": "system", "content": system_msg},
          {"role": "user", "content": user_msg}
        ], # TODO: Make dynamic
        tools=tools
      )
    except Exception as e:
      raise Exception(f"Failed to retrieve response from OpenAI | {str(e)}")

    try:
      # Parse JSON data from OpenAI's response
      tool_call = response.choices[0].message.tool_calls[0]
      arguments = tool_call.function.arguments
      resume_data = json.loads(arguments)
    except Exception as e:
      raise Exception(f"Failed to parse resume JSON data from OpenAI's response | {str(e)}")

    return resume_data
