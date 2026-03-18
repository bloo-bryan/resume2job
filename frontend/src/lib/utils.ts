import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { SCORE_TIERS } from "./constants";
import type { MatchBreakdown } from "./types";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getScoreTier(score: number) {
  if (score >= SCORE_TIERS.strong.min) return SCORE_TIERS.strong;
  if (score >= SCORE_TIERS.moderate.min) return SCORE_TIERS.moderate;
  return SCORE_TIERS.weak;
}

export function formatPercent(score: number): string {
  return `${Math.round(score * 100)}%`;
}

export function getBreakdownScore(
  breakdown: MatchBreakdown,
  key: string
): number {
  switch (key) {
    case "required_skills":
      return breakdown.required_skills.score;
    case "semantic":
      return breakdown.semantic_similarity;
    case "experience":
      return breakdown.experience.score;
    case "education":
      return breakdown.education.score;
    case "preferred_skills":
      return breakdown.preferred_skills.score;
    default:
      return 0;
  }
}
