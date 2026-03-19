"use client";

import { WEIGHT_CONFIG } from "@/lib/constants";
import type { MatchBreakdown } from "@/lib/types";
import { cn, formatPercent, getBreakdownScore, getScoreTier } from "@/lib/utils";

interface SignalBarProps {
  breakdown: MatchBreakdown;
}

export function SignalBar({ breakdown }: SignalBarProps) {
  // Build dynamic aria-label describing all segments
  const ariaLabel = WEIGHT_CONFIG.map((w) => {
    const score = getBreakdownScore(breakdown, w.key);
    const tier = getScoreTier(score);
    return `${w.label} ${formatPercent(score)} ${tier.label.toLowerCase().replace(" match", "")}`;
  }).join(", ");

  return (
    <div className="space-y-3">
      {/* Bar */}
      <div
        role="img"
        aria-label={`Match breakdown: ${ariaLabel}`}
        className="flex gap-0.5 h-3 rounded-full overflow-hidden"
      >
        {WEIGHT_CONFIG.map((w) => {
          const score = getBreakdownScore(breakdown, w.key);
          const tier = getScoreTier(score);
          return (
            <div
              key={w.key}
              aria-hidden="true"
              className={cn("transition-all", tier.bg)}
              style={{ width: `${w.weight * 100}%`, opacity: 0.2 + score * 0.8 }}
            />
          );
        })}
      </div>

      {/* Screen reader summary */}
      <span className="sr-only">
        Match breakdown: {ariaLabel}
      </span>

      {/* Legend — horizontal on desktop, vertical on mobile */}
      <div className="hidden sm:flex items-center gap-4">
        {WEIGHT_CONFIG.map((w) => {
          const score = getBreakdownScore(breakdown, w.key);
          const tier = getScoreTier(score);
          return (
            <div key={w.key} className="flex items-center gap-1.5">
              <div className={cn("w-2.5 h-2.5 rounded-full", tier.bg)} />
              <span className="text-xs text-zinc-400">{w.label}</span>
              <span className={cn("text-xs font-mono", tier.color)}>
                {formatPercent(score)}
              </span>
            </div>
          );
        })}
      </div>

      {/* Mobile: vertical list with progress bars */}
      <div className="flex flex-col gap-1.5 sm:hidden">
        {WEIGHT_CONFIG.map((w) => {
          const score = getBreakdownScore(breakdown, w.key);
          const tier = getScoreTier(score);
          return (
            <div key={w.key} className="space-y-0.5">
              <div className="flex items-center justify-between">
                <span className="text-xs text-zinc-400">
                  {w.label} ({Math.round(w.weight * 100)}%)
                </span>
                <span className={cn("text-xs font-mono", tier.color)}>
                  {formatPercent(score)}
                </span>
              </div>
              <div className="h-1 w-full rounded-full bg-zinc-800 overflow-hidden">
                <div
                  className={cn("h-full rounded-full", tier.bg)}
                  style={{ width: `${score * 100}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
