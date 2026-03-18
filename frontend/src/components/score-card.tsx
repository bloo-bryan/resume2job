import { cn, formatPercent, getScoreTier } from "@/lib/utils";

interface ScoreCardProps {
  label: string;
  score: number;
  detail?: string;
}

export function ScoreCard({ label, score, detail }: ScoreCardProps) {
  const tier = getScoreTier(score);

  return (
    <div className="rounded-md border border-zinc-800 bg-zinc-900 p-4 space-y-2">
      <p className="text-xs uppercase tracking-wider text-zinc-400">{label}</p>
      <p className={cn("text-3xl font-mono font-semibold", tier.color)}>
        {formatPercent(score)}
      </p>
      <div className="h-1 w-full rounded-full bg-zinc-800 overflow-hidden">
        <div
          className={cn("h-full rounded-full transition-all", tier.bg)}
          style={{ width: `${score * 100}%` }}
        />
      </div>
      {detail && <p className="text-xs text-zinc-500">{detail}</p>}
    </div>
  );
}
