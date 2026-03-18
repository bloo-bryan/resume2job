"use client";

import { useState } from "react";
import { SignalBar } from "./signal-bar";
import { ScoreCard } from "./score-card";
import { SkillTags } from "./skill-tags";
import { Alert, AlertDescription } from "@/components/ui/alert";
import type { MatchBreakdown as MatchBreakdownType } from "@/lib/types";

interface MatchBreakdownProps {
  breakdown: MatchBreakdownType;
  summary: string;
}

export function MatchBreakdownPanel({
  breakdown,
  summary,
}: MatchBreakdownProps) {
  const [detailsOpen, setDetailsOpen] = useState(false);

  return (
    <div className="space-y-6">
      {/* Summary */}
      <Alert className="border-blue-500/20 bg-blue-500/5">
        <AlertDescription className="text-sm text-zinc-300">
          {summary}
        </AlertDescription>
      </Alert>

      {/* Signal Bar */}
      <SignalBar breakdown={breakdown} />

      {/* Score Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <ScoreCard
          label="Required Skills"
          score={breakdown.required_skills.score}
          detail={`${breakdown.required_skills.matched.length} matched, ${breakdown.required_skills.missing.length} missing`}
        />
        <ScoreCard
          label="Semantic Similarity"
          score={breakdown.semantic_similarity}
        />
        <ScoreCard
          label="Experience"
          score={breakdown.experience.score}
          detail={`Required: ${breakdown.experience.required ?? "N/A"} yrs | Detected: ${breakdown.experience.detected} yrs`}
        />
        <ScoreCard
          label="Education"
          score={breakdown.education.score}
          detail={`Required: ${breakdown.education.required ?? "N/A"} | Detected: ${breakdown.education.detected ?? "N/A"}`}
        />
      </div>

      {/* Expandable Details */}
      <button
        onClick={() => setDetailsOpen(!detailsOpen)}
        className="text-sm text-zinc-400 hover:text-zinc-200 transition-colors"
      >
        {detailsOpen ? "Hide" : "Show"} skill details
      </button>

      {detailsOpen && (
        <div className="space-y-4">
          <div>
            <p className="text-xs uppercase tracking-wider text-zinc-400 mb-2">
              Required Skills
            </p>
            <SkillTags
              matched={breakdown.required_skills.matched}
              missing={breakdown.required_skills.missing}
            />
          </div>
          <div>
            <p className="text-xs uppercase tracking-wider text-zinc-400 mb-2">
              Preferred Skills
            </p>
            <SkillTags
              matched={breakdown.preferred_skills.matched}
              missing={breakdown.preferred_skills.missing}
            />
          </div>
        </div>
      )}
    </div>
  );
}
