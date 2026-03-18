"use client";

import { useState } from "react";
import { ResumeInput } from "@/components/resume-input";
import { JdInput } from "@/components/jd-input";
import { MatchBreakdownPanel } from "@/components/match-breakdown";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { matchResume } from "@/lib/api";
import { ALGORITHM_LABELS } from "@/lib/constants";
import { cn, formatPercent, getScoreTier } from "@/lib/utils";
import type { MatchResult, Algorithm } from "@/lib/types";

export default function MatchPage() {
  const [resumeText, setResumeText] = useState("");
  const [jdText, setJdText] = useState("");
  const [algorithm, setAlgorithm] = useState<Algorithm>("hybrid");
  const [result, setResult] = useState<MatchResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canSubmit = resumeText.trim() && jdText.trim() && !loading;

  async function handleSubmit() {
    setLoading(true);
    setError(null);
    try {
      const data = await matchResume({
        resume_text: resumeText,
        jd_text: jdText,
        algorithm,
      });
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Match</h1>
        <p className="text-sm text-zinc-400 mt-1">
          Score a resume against a job description
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ResumeInput
          text={resumeText}
          onTextChange={setResumeText}
          disabled={loading}
        />
        <JdInput value={jdText} onChange={setJdText} disabled={loading} />
      </div>

      <div className="flex items-center gap-4">
        <select
          value={algorithm}
          onChange={(e) => setAlgorithm(e.target.value as Algorithm)}
          disabled={loading}
          className="h-9 rounded-md border border-zinc-800 bg-zinc-900 px-3 text-sm text-zinc-100"
        >
          {(["hybrid", "tfidf", "embedding"] as const).map((a) => (
            <option key={a} value={a}>
              {ALGORITHM_LABELS[a]}
            </option>
          ))}
        </select>

        <Button onClick={handleSubmit} disabled={!canSubmit}>
          {loading ? "Analyzing..." : "Analyze Match"}
        </Button>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {result && (
        <div className="space-y-6">
          <div className="flex items-baseline gap-4">
            <span
              className={cn(
                "text-5xl font-mono font-bold",
                getScoreTier(result.overall_score).color
              )}
            >
              {formatPercent(result.overall_score)}
            </span>
            <span
              className={cn(
                "text-sm",
                getScoreTier(result.overall_score).color
              )}
            >
              {getScoreTier(result.overall_score).label}
            </span>
          </div>

          <MatchBreakdownPanel
            breakdown={result.breakdown}
            summary={result.summary}
          />
        </div>
      )}

      {!result && !error && !loading && (
        <p className="text-sm text-zinc-500 text-center py-8">
          Upload a resume and paste a job description to get started
        </p>
      )}
    </div>
  );
}
