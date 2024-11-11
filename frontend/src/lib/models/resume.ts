export interface ResumeDetails {
  id: string;
  base_requirement_satisfaction_score: number;
  exceptional_considerations: string;
  fitness_score: number;
}

export interface ListClassifiedResponse {
  very_fit: ResumeDetails[];
  fit: ResumeDetails[];
  not_fit: ResumeDetails[];
}
