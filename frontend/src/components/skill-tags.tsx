import { cn } from "@/lib/utils";

interface SkillTagsProps {
  matched: string[];
  missing: string[];
  preferred?: string[];
}

export function SkillTags({ matched, missing, preferred }: SkillTagsProps) {
  return (
    <div className="flex flex-wrap gap-1.5">
      {matched.map((skill) => (
        <span
          key={`m-${skill}`}
          className="inline-flex items-center gap-1 rounded-full bg-green-500/15 px-2.5 py-0.5 text-sm text-green-500"
        >
          <svg className="w-3 h-3" viewBox="0 0 12 12" fill="none">
            <path
              d="M2 6l3 3 5-5"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          {skill}
        </span>
      ))}
      {preferred?.map((skill) => (
        <span
          key={`p-${skill}`}
          className={cn(
            "inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-sm",
            "bg-yellow-500/15 text-yellow-500"
          )}
        >
          {skill}
        </span>
      ))}
      {missing.map((skill) => (
        <span
          key={`x-${skill}`}
          className="inline-flex items-center gap-1 rounded-full bg-red-500/15 px-2.5 py-0.5 text-sm text-red-500"
        >
          <svg className="w-3 h-3" viewBox="0 0 12 12" fill="none">
            <path
              d="M3 3l6 6M9 3l-6 6"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
            />
          </svg>
          {skill}
        </span>
      ))}
    </div>
  );
}
