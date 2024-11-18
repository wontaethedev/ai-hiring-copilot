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
  ASSESSED_FIT = "processed_fit",
  ASSESSED_UNFIT = "processed_unfit",
}
