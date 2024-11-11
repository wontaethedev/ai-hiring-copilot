from enum import StrEnum


class StatusTypes(StrEnum):
  PENDING = 'pending'
  IN_PROGRESS = 'in_progress'
  COMPLETE = 'complete'
  FAILED = 'failed'


class RoleTypes(StrEnum):
  SENIOR_PRODUCT_ENGINEER = 'senior_product_engineer'
