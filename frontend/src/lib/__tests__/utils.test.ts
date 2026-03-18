import { describe, it, expect } from "vitest";
import { getScoreTier, formatPercent, getBreakdownScore } from "../utils";
import { SCORE_TIERS } from "../constants";
import type { MatchBreakdown } from "../types";

describe("getScoreTier", () => {
  it("returns strong for scores >= 0.7", () => {
    expect(getScoreTier(0.7)).toBe(SCORE_TIERS.strong);
    expect(getScoreTier(0.85)).toBe(SCORE_TIERS.strong);
    expect(getScoreTier(1.0)).toBe(SCORE_TIERS.strong);
  });

  it("returns moderate for scores >= 0.4 and < 0.7", () => {
    expect(getScoreTier(0.4)).toBe(SCORE_TIERS.moderate);
    expect(getScoreTier(0.5)).toBe(SCORE_TIERS.moderate);
    expect(getScoreTier(0.69)).toBe(SCORE_TIERS.moderate);
  });

  it("returns weak for scores < 0.4", () => {
    expect(getScoreTier(0.0)).toBe(SCORE_TIERS.weak);
    expect(getScoreTier(0.2)).toBe(SCORE_TIERS.weak);
    expect(getScoreTier(0.39)).toBe(SCORE_TIERS.weak);
  });

  it("handles exact boundary values", () => {
    expect(getScoreTier(0.39999)).toBe(SCORE_TIERS.weak);
    expect(getScoreTier(0.4)).toBe(SCORE_TIERS.moderate);
    expect(getScoreTier(0.69999)).toBe(SCORE_TIERS.moderate);
    expect(getScoreTier(0.7)).toBe(SCORE_TIERS.strong);
  });
});

describe("formatPercent", () => {
  it("converts decimal to percentage string", () => {
    expect(formatPercent(0.85)).toBe("85%");
    expect(formatPercent(0.0)).toBe("0%");
    expect(formatPercent(1.0)).toBe("100%");
  });

  it("rounds to nearest integer", () => {
    expect(formatPercent(0.456)).toBe("46%");
    expect(formatPercent(0.454)).toBe("45%");
  });
});

const mockBreakdown: MatchBreakdown = {
  required_skills: { score: 0.8, matched: ["python"], missing: ["go"] },
  preferred_skills: { score: 0.5, matched: ["docker"], missing: [] },
  semantic_similarity: 0.72,
  experience: { score: 1.0, required: 3, detected: 5 },
  education: { score: 0.9, required: "bachelor", detected: "master" },
};

describe("getBreakdownScore", () => {
  it("extracts required_skills score", () => {
    expect(getBreakdownScore(mockBreakdown, "required_skills")).toBe(0.8);
  });

  it("extracts semantic similarity", () => {
    expect(getBreakdownScore(mockBreakdown, "semantic")).toBe(0.72);
  });

  it("extracts experience score", () => {
    expect(getBreakdownScore(mockBreakdown, "experience")).toBe(1.0);
  });

  it("extracts education score", () => {
    expect(getBreakdownScore(mockBreakdown, "education")).toBe(0.9);
  });

  it("extracts preferred_skills score", () => {
    expect(getBreakdownScore(mockBreakdown, "preferred_skills")).toBe(0.5);
  });

  it("returns 0 for unknown keys", () => {
    expect(getBreakdownScore(mockBreakdown, "nonexistent")).toBe(0);
  });
});
