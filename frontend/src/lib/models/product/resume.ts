export enum ResumeClassifierTypes {
  VERY_FIT = "very_fit",
  FIT = "fit",
  UNFIT = "unfit",
}

export enum ResumeStatusTypes {
  // System processing
  PENDING = "pending",
  IN_PROGRESS = "in_progress",
  COMPLETE = "complete",
  FAILED = "failed",

  // Human processing
  ASSESSED_FIT = "assessed_fit",
  ASSESSED_HOLD = "assessed_hold",
  ASSESSED_UNFIT = "assessed_unfit",
}

export enum ResumeCategoryTypes {
  CLASSIFIER = "classifier",
  STATUS = "status",
}
