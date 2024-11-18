from enum import StrEnum


class StatusTypes(StrEnum):
  # System processing
  PENDING = 'pending'
  IN_PROGRESS = 'in_progress'
  COMPLETE = 'complete'
  FAILED = 'failed'

  # Human processing
  ASSESSED_FIT = 'processed_fit'
  ASSESSED_UNFIT = 'processed_unfit'


class RoleTypes(StrEnum):
  # WARNING: DEPRECATED, USE `role_id` INSTEAD
  SENIOR_PRODUCT_ENGINEER = 'senior_product_engineer'
