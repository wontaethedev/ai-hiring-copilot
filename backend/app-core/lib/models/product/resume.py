from enum import StrEnum, Enum


class ClassifierTypes(Enum):
  VERY_FIT = "very_fit"
  FIT = "fit"
  UNFIT = "unfit"


class StatusTypes(StrEnum):
  # System processing
  PENDING = 'pending'
  IN_PROGRESS = 'in_progress'
  COMPLETE = 'complete'
  FAILED = 'failed'

  # Human processing
  ASSESSED_FIT = 'assessed_fit'
  ASSESSED_HOLD = 'assessed_hold'
  ASSESSED_UNFIT = 'assessed_unfit'


class RoleTypes(StrEnum):
  # WARNING: DEPRECATED, USE `role_id` INSTEAD
  SENIOR_PRODUCT_ENGINEER = 'senior_product_engineer'
