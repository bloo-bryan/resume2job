"use client";

import { WEIGHT_CONFIG } from "@/lib/constants";
import type { MatchBreakdown } from "@/lib/types";
import { cn, formatPercent, getBreakdownScore, getScoreTier } from "@/lib/utils";

interface SignalBarProps {
  breakdown: MatchBreakdown;
}

export function SignalBar({ breakdown }: SignalBarProps) {
  return (
    <div className="space-y-3">
      {/* Bar */}
      <div className="flex gap-0.5 h-3 rounded-full overflow-hidden">
        {WEIGHT_CONFIG.map((w) => {
          const score = getBreakdownScore(breakdown, w.key);
          const tier = getScoreTier(score);
          return (
            <div
              key={w.key}
              className={cn("transition-all", tier.bg)}
              style={{ width: `${w.weight * 100}%`, opacity: 0.2 + score * 0.8 }}
            />
          );
        })}
      </div>

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

      {/* Mobile: vertical list */}
      <div className="flex flex-col gap-1.5 sm:hidden">
        {WEIGHT_CONFIG.map((w) => {
          const score = getBreakdownScore(breakdown, w.key);
          const tier = getScoreTier(score);
          return (
            <div key={w.key} className="flex items-center justify-between">
              <div className="flex items-center gap-1.5">
                <div className={cn("w-2.5 h-2.5 rounded-full", tier.bg)} />
                <span className="text-xs text-zinc-400">
                  {w.label} ({Math.round(w.weight * 100)}%)
                </span>
              </div>
              <span className={cn("text-xs font-mono", tier.color)}>
                {formatPercent(score)}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
