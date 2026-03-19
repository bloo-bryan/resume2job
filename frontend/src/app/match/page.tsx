"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { ResumeInput } from "@/components/resume-input";
import { JdInput } from "@/components/jd-input";
import { MatchBreakdownPanel } from "@/components/match-breakdown";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { matchResume } from "@/lib/api";
import { ALGORITHM_LABELS } from "@/lib/constants";
import { cn, formatPercent, getScoreTier } from "@/lib/utils";
import type { MatchResult, Algorithm } from "@/lib/types";

function MatchSkeleton() {
  return (
    <div className="space-y-6" aria-hidden="true">
      <div className="skeleton h-12 w-32" />
      <div className="skeleton h-3 w-full rounded-full" />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="skeleton h-28 rounded-md" />
        ))}
      </div>
    </div>
  );
}

export default function MatchPage() {
  const [resumeText, setResumeText] = useState("");
  const [jdText, setJdText] = useState("");
  const [algorithm, setAlgorithm] = useState<Algorithm>("hybrid");
  const [result, setResult] = useState<MatchResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const resultsRef = useRef<HTMLDivElement>(null);
  const errorRef = useRef<HTMLDivElement>(null);

  const canSubmit = resumeText.trim() && jdText.trim() && !loading;

  // Read sessionStorage on mount for cross-page state transfer
  useEffect(() => {
    const sr = sessionStorage.getItem("r2j_resume");
    const sj = sessionStorage.getItem("r2j_jd");
    if (sr) setResumeText(sr);
    if (sj) setJdText(sj);
  }, []);

  async function handleSubmit() {
    setLoading(true);
    setError(null);
    // Save to sessionStorage for cross-page transfer
    sessionStorage.setItem("r2j_resume", resumeText);
    sessionStorage.setItem("r2j_jd", jdText);
    try {
      const data = await matchResume({
        resume_text: resumeText,
        jd_text: jdText,
        algorithm,
      });
      setResult(data);
      // Focus results after render
      requestAnimationFrame(() => resultsRef.current?.focus());
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
      setResult(null);
      requestAnimationFrame(() => errorRef.current?.focus());
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-semibold tracking-tight">Match</h1>
        <p className="text-sm text-zinc-400 mt-1">
          Multi-signal matching engine — TF-IDF + semantic embeddings + structured extraction, evaluated on 30 labeled pairs.
        </p>
      </div>

      <form
        aria-label="Match inputs"
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

        <div className="flex items-center gap-4 mt-6">
          <select
            value={algorithm}
            onChange={(e) => setAlgorithm(e.target.value as Algorithm)}
            disabled={loading}
            aria-label="Scoring algorithm"
            className="h-10 min-h-[44px] rounded-md border border-zinc-800 bg-zinc-900 px-3 text-sm text-zinc-100"
          >
            {(["hybrid", "tfidf", "embedding"] as const).map((a) => (
              <option key={a} value={a}>
                {ALGORITHM_LABELS[a]}
              </option>
            ))}
          </select>

          <Button
            type="submit"
            disabled={!canSubmit}
            className="min-h-[44px]"
          >
            {loading ? "Analyzing..." : "Analyze Match"}
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

      <section
        role="region"
        aria-label="Match results"
        aria-live="polite"
      >
        {loading && <MatchSkeleton />}

        {result && !loading && (
          <div ref={resultsRef} tabIndex={-1} className="space-y-6 outline-none">
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

            <Link
              href="/compare"
              className="inline-flex items-center gap-1 text-sm text-blue-500 hover:text-blue-400 transition-colors"
            >
              Compare all algorithms →
            </Link>
          </div>
        )}

        {!result && !error && !loading && (
          <p className="text-sm text-zinc-400 text-center py-8">
            Upload a resume and paste a job description to see how well they
            match. Your match breakdown will appear here with skills, experience,
            and education analysis.
          </p>
        )}
      </section>
    </div>
  );
}
