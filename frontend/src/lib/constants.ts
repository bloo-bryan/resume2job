export const ALGORITHMS = ["tfidf", "embedding", "hybrid"] as const;

export const ALGORITHM_LABELS: Record<string, string> = {
  tfidf: "TF-IDF",
  embedding: "Embedding",
  hybrid: "Hybrid",
};

export const WEIGHT_CONFIG = [
  { key: "required_skills", label: "Skills", weight: 0.4 },
  { key: "semantic", label: "Semantic", weight: 0.3 },
  { key: "experience", label: "Experience", weight: 0.15 },
  { key: "education", label: "Education", weight: 0.1 },
  { key: "preferred_skills", label: "Preferred", weight: 0.05 },
] as const;

export const SCORE_TIERS = {
  strong: {
    min: 0.7,
    label: "Strong match",
    color: "text-green-500",
    bg: "bg-green-500",
  },
  moderate: {
    min: 0.4,
    label: "Moderate match",
    color: "text-yellow-500",
    bg: "bg-yellow-500",
  },
  weak: {
    min: 0,
    label: "Weak match",
    color: "text-red-500",
    bg: "bg-red-500",
  },
} as const;
