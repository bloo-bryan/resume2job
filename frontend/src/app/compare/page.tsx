"use client";

import { useEffect, useRef, useState } from "react";
import { ResumeInput } from "@/components/resume-input";
import { JdInput } from "@/components/jd-input";
import { MatchBreakdownPanel } from "@/components/match-breakdown";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { compareAlgorithms } from "@/lib/api";
import { ALGORITHM_LABELS, ALGORITHMS } from "@/lib/constants";
import { cn, formatPercent, getScoreTier } from "@/lib/utils";
import type { CompareResult } from "@/lib/types";

function CompareSkeleton() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6" aria-hidden="true">
      {Array.from({ length: 3 }).map((_, i) => (
        <div key={i} className="space-y-4 rounded-lg border border-zinc-800 bg-zinc-900/50 p-5">
          <div className="skeleton h-8 w-24" />
          <div className="skeleton h-3 w-full rounded-full" />
          <div className="grid grid-cols-2 gap-3">
            {Array.from({ length: 4 }).map((_, j) => (
              <div key={j} className="skeleton h-20 rounded-md" />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export default function ComparePage() {
  const [resumeText, setResumeText] = useState("");
  const [jdText, setJdText] = useState("");
  const [result, setResult] = useState<CompareResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const resultsRef = useRef<HTMLDivElement>(null);
  const errorRef = useRef<HTMLDivElement>(null);

  const canSubmit = resumeText.trim() && jdText.trim() && !loading;

  // Read sessionStorage on mount
  useEffect(() => {
    const sr = sessionStorage.getItem("r2j_resume");
    const sj = sessionStorage.getItem("r2j_jd");
    if (sr) setResumeText(sr);
    if (sj) setJdText(sj);
  }, []);

  async function handleSubmit() {
    setLoading(true);
    setError(null);
    sessionStorage.setItem("r2j_resume", resumeText);
    sessionStorage.setItem("r2j_jd", jdText);
    try {
      const data = await compareAlgorithms({
        resume_text: resumeText,
        jd_text: jdText,
      });
      setResult(data);
      requestAnimationFrame(() => resultsRef.current?.focus());
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
      setResult(null);
      requestAnimationFrame(() => errorRef.current?.focus());
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
        <h1 className="text-4xl font-semibold tracking-tight">Compare</h1>
        <p className="text-sm text-zinc-400 mt-1">
          Compare all three scoring algorithms on the same inputs
        </p>
      </div>

      <form
        aria-label="Compare inputs"
        onSubmit={(e) => {
          e.preventDefault();
          if (canSubmit) handleSubmit();
        }}
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <ResumeInput
            text={resumeText}
            onTextChange={setResumeText}
            disabled={loading}
          />
          <JdInput value={jdText} onChange={setJdText} disabled={loading} />
        </div>

        <div className="mt-6">
          <Button type="submit" disabled={!canSubmit} className="min-h-[44px]">
            {loading ? "Comparing..." : "Compare All Algorithms"}
          </Button>
        </div>
      </form>

      {error && (
        <div ref={errorRef} tabIndex={-1} className="outline-none">
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        </div>
      )}

      <section role="region" aria-label="Comparison results" aria-live="polite">
        {loading && <CompareSkeleton />}

        {result && !loading && (
          <div ref={resultsRef} tabIndex={-1} className="space-y-6 outline-none">
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
          <p className="text-sm text-zinc-400 text-center py-8">
            Upload a resume and paste a job description to compare how three
            different algorithms score the match.
          </p>
        )}
      </section>
    </div>
  );
}
