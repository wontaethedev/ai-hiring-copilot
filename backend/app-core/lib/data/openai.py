from lib.models.product.resume import RoleTypes


TOOLS: dict[RoleTypes] = {
  RoleTypes.SENIOR_PRODUCT_ENGINEER: {
    "type": "function",
    "function": {
      "name": "get_resume_assessment",
      "description": """
        Evaluates resumes for candidates applying to a senior product engineer position, providing detailed assessments to streamline the hiring process.
        This includes:
          1. Assessing whether the candidate meets the baseline qualifications and technical requirements of the role.
          2. Highlighting any standout skills, experiences, or achievements that make the candidate particularly exceptional.
          3. Generating an overall fitness score.
      """,
      "parameters": {
        "type": "object",
        "properties": {
          "base_requirement_satisfaction_score": {
            "type": "integer",
            "description": "An integer representing how well the candidate meets, with respect to the provided job description. This score must be out of 100"
          },
          "exceptionals": {
            "type": "string",
            "description": "A string describing what may make this candidate particularly exceptional or stand out."
          },
          "fitness_score": {
            "type": "integer",
            "description": "An integer representing the overall fitness score of the candidate for role, with respect to the provided job description. This score must be out of 100"
          },
        },
        "required": ["base_requirement_satisfaction_score", "exceptionals", "fitness_score"],
        "additionalProperties": False,
      }
    }
  }
}
