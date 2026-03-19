"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";

interface SkillTagsProps {
  matched: string[];
  missing: string[];
  preferred?: string[];
}

const INITIAL_LIMIT = 10;

export function SkillTags({ matched, missing, preferred }: SkillTagsProps) {
  const [showAllMatched, setShowAllMatched] = useState(false);
  const [showAllMissing, setShowAllMissing] = useState(false);

  const visibleMatched = showAllMatched ? matched : matched.slice(0, INITIAL_LIMIT);
  const visibleMissing = showAllMissing ? missing : missing.slice(0, INITIAL_LIMIT);

  return (
    <div className="flex flex-wrap gap-1.5">
      {visibleMatched.map((skill) => (
        <span
          key={`m-${skill}`}
          className="inline-flex items-center gap-1 rounded-full bg-green-500/15 px-2.5 py-0.5 text-sm text-green-500 max-w-[200px]"
        >
          <svg className="w-3 h-3 shrink-0" viewBox="0 0 12 12" fill="none">
            <path
              d="M2 6l3 3 5-5"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <span className="truncate">{skill}</span>
        </span>
      ))}
      {matched.length > INITIAL_LIMIT && !showAllMatched && (
        <button
          onClick={() => setShowAllMatched(true)}
          className="text-sm text-zinc-400 hover:underline hover:text-zinc-200 transition-colors"
        >
          Show all {matched.length} matched
        </button>
      )}

      {preferred?.map((skill) => (
        <span
          key={`p-${skill}`}
          className={cn(
            "inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-sm max-w-[200px]",
            "bg-yellow-500/15 text-yellow-500"
          )}
        >
          <span className="truncate">{skill}</span>
        </span>
      ))}

      {visibleMissing.map((skill) => (
        <span
          key={`x-${skill}`}
          className="inline-flex items-center gap-1 rounded-full bg-red-500/15 px-2.5 py-0.5 text-sm text-red-500 max-w-[200px]"
        >
          <svg className="w-3 h-3 shrink-0" viewBox="0 0 12 12" fill="none">
            <path
              d="M3 3l6 6M9 3l-6 6"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
            />
          </svg>
          <span className="truncate">{skill}</span>
        </span>
      ))}
      {missing.length > INITIAL_LIMIT && !showAllMissing && (
        <button
          onClick={() => setShowAllMissing(true)}
          className="text-sm text-zinc-400 hover:underline hover:text-zinc-200 transition-colors"
        >
          Show all {missing.length} missing
        </button>
      )}
    </div>
  );
}
