// --- Domain Models (from models.py) ---

export interface Position {
  title: string;
  company: string | null;
  start_date: string | null;
  end_date: string | null;
  years: number | null;
}

export interface ExperienceInfo {
  total_years: number;
  positions: Position[];
}

export interface EducationEntry {
  degree: string;
  field: string | null;
  institution: string | null;
}

export interface ResumeEntities {
  skills: string[];
  experience: ExperienceInfo;
  education: EducationEntry[];
}

export interface JobDescriptionEntities {
  required_skills: string[];
  preferred_skills: string[];
  min_experience_years: number | null;
  required_education: string | null;
}

export type ParseResult =
  | { raw_text: string; cleaned_text: string; doc_type: "resume"; entities: ResumeEntities }
  | { raw_text: string; cleaned_text: string; doc_type: "job_description"; entities: JobDescriptionEntities };

export interface SkillsBreakdown {
  score: number;
  matched: string[];
  missing: string[];
}

export interface ExperienceBreakdown {
  score: number;
  required: number | null;
  detected: number;
}

export interface EducationBreakdown {
  score: number;
  required: string | null;
  detected: string | null;
}

export interface MatchBreakdown {
  required_skills: SkillsBreakdown;
  preferred_skills: SkillsBreakdown;
  semantic_similarity: number;
  experience: ExperienceBreakdown;
  education: EducationBreakdown;
}

export interface MatchResult {
  overall_score: number;
  breakdown: MatchBreakdown;
  summary: string;
}

export interface CompareResult {
  tfidf: MatchResult;
  embedding: MatchResult;
  hybrid: MatchResult;
}

// --- API Schemas (from schemas.py) ---

export interface MatchRequest {
  resume_text: string;
  jd_text: string;
  algorithm?: "hybrid" | "tfidf" | "embedding";
  weights?: Record<string, number>;
}

export interface CompareRequest {
  resume_text: string;
  jd_text: string;
  weights?: Record<string, number>;
}

export interface HealthResponse {
  status: "healthy" | "unhealthy";
  models_loaded: boolean;
  qdrant_connected: boolean;
}

export interface AlgorithmMetrics {
  ndcg_at_5: number;
  mrr: number;
  precision_at_3: number;
}

export interface EvaluationResult {
  test_set_size: number;
  tfidf: AlgorithmMetrics;
  embedding: AlgorithmMetrics;
  hybrid: AlgorithmMetrics;
}

// --- Utility Types ---

export type Algorithm = "hybrid" | "tfidf" | "embedding";
export type DocType = "resume" | "job_description";
export type ScoreTier = "strong" | "moderate" | "weak";
