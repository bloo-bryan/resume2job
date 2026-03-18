"use client";

import { useState } from "react";
import { ResumeInput } from "@/components/resume-input";
import { JdInput } from "@/components/jd-input";
import { MatchBreakdownPanel } from "@/components/match-breakdown";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { compareAlgorithms } from "@/lib/api";
import { ALGORITHM_LABELS, ALGORITHMS } from "@/lib/constants";
import { cn, formatPercent, getScoreTier } from "@/lib/utils";
import type { CompareResult } from "@/lib/types";

export default function ComparePage() {
  const [resumeText, setResumeText] = useState("");
  const [jdText, setJdText] = useState("");
  const [result, setResult] = useState<CompareResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canSubmit = resumeText.trim() && jdText.trim() && !loading;

  async function handleSubmit() {
    setLoading(true);
    setError(null);
    try {
      const data = await compareAlgorithms({
        resume_text: resumeText,
        jd_text: jdText,
      });
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  }

  const scores = result
    ? ALGORITHMS.map((a) => result[a].overall_score)
    : [];
  const maxDelta =
    scores.length > 0 ? Math.max(...scores) - Math.min(...scores) : 0;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Compare</h1>
        <p className="text-sm text-zinc-400 mt-1">
          Compare all three scoring algorithms on the same inputs
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

      <Button onClick={handleSubmit} disabled={!canSubmit}>
        {loading ? "Comparing..." : "Compare All Algorithms"}
      </Button>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {result && (
        <div className="space-y-6">
          {maxDelta > 0.1 && (
            <Alert className="border-yellow-500/20 bg-yellow-500/5">
              <AlertDescription className="text-sm text-yellow-500">
                Algorithms disagree significantly (max delta:{" "}
                {formatPercent(maxDelta)}). Review the breakdowns to understand
                why.
              </AlertDescription>
            </Alert>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {ALGORITHMS.map((algo) => {
              const algoResult = result[algo];
              const tier = getScoreTier(algoResult.overall_score);
              return (
                <div
                  key={algo}
                  className="rounded-lg border border-zinc-800 bg-zinc-900/50 p-5 space-y-4"
                >
                  <div className="flex items-baseline justify-between">
                    <h3 className="text-lg font-semibold">
                      {ALGORITHM_LABELS[algo]}
                    </h3>
                    <span
                      className={cn("text-3xl font-mono font-bold", tier.color)}
                    >
                      {formatPercent(algoResult.overall_score)}
                    </span>
                  </div>
                  <MatchBreakdownPanel
                    breakdown={algoResult.breakdown}
                    summary={algoResult.summary}
                  />
                </div>
              );
            })}
          </div>
        </div>
      )}

      {!result && !error && !loading && (
        <p className="text-sm text-zinc-500 text-center py-8">
          Upload a resume and paste a job description, then compare all
          algorithms
        </p>
      )}
    </div>
  );
}
