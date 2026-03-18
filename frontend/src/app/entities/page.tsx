"use client";

import { useState } from "react";
import { ResumeInput } from "@/components/resume-input";
import { JdInput } from "@/components/jd-input";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { parseDocument } from "@/lib/api";
import type {
  ResumeEntities,
  JobDescriptionEntities,
} from "@/lib/types";

export default function EntitiesPage() {
  const [resumeText, setResumeText] = useState("");
  const [jdText, setJdText] = useState("");
  const [resumeEntities, setResumeEntities] = useState<ResumeEntities | null>(null);
  const [jdEntities, setJdEntities] = useState<JobDescriptionEntities | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canSubmit = (resumeText.trim() || jdText.trim()) && !loading;

  async function handleSubmit() {
    setLoading(true);
    setError(null);
    setResumeEntities(null);
    setJdEntities(null);

    const promises: Promise<PromiseSettledResult<void>>[] = [];

    const resumePromise = resumeText.trim()
      ? parseDocument(resumeText, "resume").then((r) => {
          if (r.doc_type === "resume") setResumeEntities(r.entities);
        })
      : null;

    const jdPromise = jdText.trim()
      ? parseDocument(jdText, "job_description").then((r) => {
          if (r.doc_type === "job_description") setJdEntities(r.entities);
        })
      : null;

    const settled = await Promise.allSettled(
      [resumePromise, jdPromise].filter(Boolean) as Promise<void>[]
    );

    const failures = settled
      .filter((r): r is PromiseRejectedResult => r.status === "rejected")
      .map((r) => (r.reason instanceof Error ? r.reason.message : "An error occurred"));

    if (failures.length > 0) {
      setError(failures.join("; "));
    }

    setLoading(false);
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Entities</h1>
        <p className="text-sm text-zinc-400 mt-1">
          Extract structured entities from resumes and job descriptions
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
        {loading ? "Extracting..." : "Extract Entities"}
      </Button>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {(resumeEntities || jdEntities) && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {resumeEntities && (
            <ResumeEntitiesPanel entities={resumeEntities} />
          )}
          {jdEntities && (
            <JdEntitiesPanel entities={jdEntities} />
          )}
        </div>
      )}

      {!resumeEntities && !jdEntities && !error && !loading && (
        <p className="text-sm text-zinc-500 text-center py-8">
          Provide a resume or job description to extract entities
        </p>
      )}
    </div>
  );
}

function ResumeEntitiesPanel({ entities }: { entities: ResumeEntities }) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-900/50 p-5 space-y-4">
      <h3 className="text-lg font-semibold">Resume Entities</h3>

      <div>
        <p className="text-xs uppercase tracking-wider text-zinc-400 mb-2">
          Skills
        </p>
        {entities.skills.length > 0 ? (
          <div className="flex flex-wrap gap-1.5">
            {entities.skills.map((s) => (
              <span
                key={s}
                className="rounded-full bg-zinc-800 px-2.5 py-0.5 text-sm text-zinc-300"
              >
                {s}
              </span>
            ))}
          </div>
        ) : (
          <p className="text-sm text-zinc-500">No skills detected</p>
        )}
      </div>

      <div>
        <p className="text-xs uppercase tracking-wider text-zinc-400 mb-2">
          Experience
        </p>
        <p className="text-sm font-mono text-zinc-200">
          {entities.experience.total_years} years
        </p>
        {entities.experience.positions.map((pos, i) => (
          <p key={i} className="text-sm text-zinc-400 mt-1">
            {pos.title}
            {pos.company ? ` at ${pos.company}` : ""}
          </p>
        ))}
      </div>

      <div>
        <p className="text-xs uppercase tracking-wider text-zinc-400 mb-2">
          Education
        </p>
        {entities.education.map((edu, i) => (
          <p key={i} className="text-sm text-zinc-400">
            {[edu.degree, edu.field, edu.institution]
              .filter(Boolean)
              .join(", ")}
          </p>
        ))}
      </div>
    </div>
  );
}

function JdEntitiesPanel({
  entities,
}: {
  entities: JobDescriptionEntities;
}) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-900/50 p-5 space-y-4">
      <h3 className="text-lg font-semibold">Job Description Entities</h3>

      <div>
        <p className="text-xs uppercase tracking-wider text-zinc-400 mb-2">
          Required Skills
        </p>
        {entities.required_skills.length > 0 ? (
          <div className="flex flex-wrap gap-1.5">
            {entities.required_skills.map((s) => (
              <span
                key={s}
                className="rounded-full bg-zinc-800 px-2.5 py-0.5 text-sm text-zinc-300"
              >
                {s}
              </span>
            ))}
          </div>
        ) : (
          <p className="text-sm text-zinc-500">None detected</p>
        )}
      </div>

      <div>
        <p className="text-xs uppercase tracking-wider text-zinc-400 mb-2">
          Preferred Skills
        </p>
        {entities.preferred_skills.length > 0 ? (
          <div className="flex flex-wrap gap-1.5">
            {entities.preferred_skills.map((s) => (
              <span
                key={s}
                className="rounded-full bg-yellow-500/15 px-2.5 py-0.5 text-sm text-yellow-500"
              >
                {s}
              </span>
            ))}
          </div>
        ) : (
          <p className="text-sm text-zinc-500">None detected</p>
        )}
      </div>

      <div>
        <p className="text-xs uppercase tracking-wider text-zinc-400 mb-2">
          Min Experience
        </p>
        <p className="text-sm font-mono text-zinc-200">
          {entities.min_experience_years !== null
            ? `${entities.min_experience_years} years`
            : "N/A"}
        </p>
      </div>

      <div>
        <p className="text-xs uppercase tracking-wider text-zinc-400 mb-2">
          Required Education
        </p>
        <p className="text-sm text-zinc-200">
          {entities.required_education ?? "N/A"}
        </p>
      </div>
    </div>
  );
}
