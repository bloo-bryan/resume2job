import evaluationData from "../../../public/evaluation_results.json";
import { ALGORITHM_LABELS, ALGORITHMS } from "@/lib/constants";
import type { EvaluationResult } from "@/lib/types";
import { cn } from "@/lib/utils";

const data = evaluationData as EvaluationResult;

const METRICS = [
  { key: "ndcg_at_5" as const, label: "NDCG@5" },
  { key: "mrr" as const, label: "MRR" },
  { key: "precision_at_3" as const, label: "P@3" },
];

export default function EvaluationPage() {
  // Find best value per metric
  const bestPerMetric: Record<string, number> = {};
  for (const m of METRICS) {
    bestPerMetric[m.key] = Math.max(
      ...ALGORITHMS.map((a) => data[a][m.key])
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Evaluation</h1>
        <p className="text-sm text-zinc-400 mt-1">
          Benchmark results across scoring algorithms
        </p>
      </div>

      <div className="inline-flex items-baseline gap-2 rounded-md border border-zinc-800 bg-zinc-900 px-4 py-3">
        <span className="text-xs uppercase tracking-wider text-zinc-400">
          Test Set Size
        </span>
        <span className="text-2xl font-mono font-semibold text-zinc-100">
          {data.test_set_size}
        </span>
        <span className="text-sm text-zinc-500">pairs</span>
      </div>

      {/* Metrics Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-zinc-800">
              <th className="text-left text-xs uppercase tracking-wider text-zinc-500 pb-3 pr-6">
                Algorithm
              </th>
              {METRICS.map((m) => (
                <th
                  key={m.key}
                  className="text-right text-xs uppercase tracking-wider text-zinc-500 pb-3 px-4"
                >
                  {m.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {ALGORITHMS.map((algo) => (
              <tr key={algo} className="border-b border-zinc-800/50">
                <td className="py-3 pr-6 font-medium text-zinc-200">
                  {ALGORITHM_LABELS[algo]}
                </td>
                {METRICS.map((m) => {
                  const val = data[algo][m.key];
                  const isBest = val === bestPerMetric[m.key];
                  return (
                    <td
                      key={m.key}
                      className={cn(
                        "py-3 px-4 text-right font-mono",
                        isBest ? "text-green-500" : "text-zinc-300"
                      )}
                    >
                      {val.toFixed(4)}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Deltas vs TF-IDF */}
      <div>
        <h2 className="text-lg font-semibold mb-3">
          Pairwise NDCG@5 Deltas (vs TF-IDF baseline)
        </h2>
        <div className="space-y-1">
          {(["embedding", "hybrid"] as const).map((algo) => {
            const delta = data[algo].ndcg_at_5 - data.tfidf.ndcg_at_5;
            return (
              <div key={algo} className="flex items-center gap-3">
                <span className="text-sm text-zinc-400 w-24">
                  {ALGORITHM_LABELS[algo]}
                </span>
                <span
                  className={cn(
                    "font-mono text-sm",
                    delta > 0
                      ? "text-green-500"
                      : delta < 0
                        ? "text-red-500"
                        : "text-zinc-400"
                  )}
                >
                  {delta >= 0 ? "+" : ""}
                  {delta.toFixed(4)}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Best algorithm */}
      {data.hybrid.ndcg_at_5 >= data.tfidf.ndcg_at_5 && (
        <div className="rounded-md border border-green-500/20 bg-green-500/5 px-4 py-3">
          <p className="text-sm text-green-500">
            Hybrid matches or outperforms TF-IDF baseline on NDCG@5
          </p>
        </div>
      )}
    </div>
  );
}
