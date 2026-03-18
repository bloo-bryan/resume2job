import argparse
import json
import logging
from collections import defaultdict
from dataclasses import asdict, dataclass

from resume2job.evaluation.dataset import load_test_set, load_texts
from resume2job.evaluation.metrics import mrr, ndcg_at_k, precision_at_k
from resume2job.extraction import extract_jd_entities, extract_resume_entities
from resume2job.extraction.ner import build_nlp_pipeline
from resume2job.parser.text_cleaner import clean_text
from resume2job.scoring import match

logger = logging.getLogger(__name__)

ALGORITHMS = ("tfidf", "embedding", "hybrid")


@dataclass
class AlgorithmMetrics:
    ndcg_at_5: float
    mrr: float
    precision_at_3: float


@dataclass
class BenchmarkResult:
    test_set_size: int
    tfidf: AlgorithmMetrics
    embedding: AlgorithmMetrics
    hybrid: AlgorithmMetrics


def run_benchmark() -> BenchmarkResult:
    test_set = load_test_set()
    nlp = build_nlp_pipeline()

    # Group pairs by JD (each JD = one query)
    queries: dict[str, list[tuple[str, int]]] = defaultdict(list)
    jd_texts: dict[str, str] = {}

    for pair in test_set.pairs:
        resume_text, jd_text = load_texts(pair)
        cleaned_resume = clean_text(resume_text)
        cleaned_jd = clean_text(jd_text)

        if pair.jd_file not in jd_texts:
            jd_texts[pair.jd_file] = cleaned_jd

        queries[pair.jd_file].append((cleaned_resume, pair.relevance))

    # Score each query with each algorithm
    algo_relevances: dict[str, list[list[float]]] = {algo: [] for algo in ALGORITHMS}

    for jd_file, resume_pairs in queries.items():
        cleaned_jd = jd_texts[jd_file]
        jd_entities = extract_jd_entities(cleaned_jd, nlp)

        for algo in ALGORITHMS:
            scored = []
            for cleaned_resume, relevance in resume_pairs:
                resume_entities = extract_resume_entities(cleaned_resume, nlp)
                result = match(
                    cleaned_resume, cleaned_jd, resume_entities, jd_entities, algorithm=algo
                )
                scored.append((result.overall_score, relevance))

            # Sort by predicted score descending, extract relevances in that order
            scored.sort(key=lambda x: x[0], reverse=True)
            ordered_rels = [rel for _, rel in scored]
            algo_relevances[algo].append(ordered_rels)

    # Compute average metrics per algorithm
    algo_metrics = {}
    for algo in ALGORITHMS:
        all_rels = algo_relevances[algo]
        avg_ndcg = sum(ndcg_at_k(rels, 5) for rels in all_rels) / len(all_rels)
        avg_mrr = sum(mrr(rels) for rels in all_rels) / len(all_rels)
        avg_prec = sum(precision_at_k(rels, 3) for rels in all_rels) / len(all_rels)
        algo_metrics[algo] = AlgorithmMetrics(
            ndcg_at_5=round(avg_ndcg, 4),
            mrr=round(avg_mrr, 4),
            precision_at_3=round(avg_prec, 4),
        )

    return BenchmarkResult(
        test_set_size=len(test_set.pairs),
        tfidf=algo_metrics["tfidf"],
        embedding=algo_metrics["embedding"],
        hybrid=algo_metrics["hybrid"],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run resume2job evaluation benchmark")
    parser.add_argument(
        "--json", action="store_true", dest="json_output", help="Output results as JSON"
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    print("Running benchmark...", file=__import__("sys").stderr)
    result = run_benchmark()

    if args.json_output:
        print(json.dumps(asdict(result), indent=2))
        raise SystemExit(0)

    print(f"\nTest set size: {result.test_set_size} pairs\n")
    print(f"{'Algorithm':<12} {'NDCG@5':>8} {'MRR':>8} {'P@3':>8}")
    print("-" * 40)
    for algo_name in ALGORITHMS:
        m = getattr(result, algo_name)
        print(f"{algo_name:<12} {m.ndcg_at_5:>8.4f} {m.mrr:>8.4f} {m.precision_at_3:>8.4f}")

    print("\nPairwise NDCG@5 deltas (vs TF-IDF baseline):")
    for algo_name in ("embedding", "hybrid"):
        m = getattr(result, algo_name)
        delta = m.ndcg_at_5 - result.tfidf.ndcg_at_5
        print(f"  {algo_name:<12} {delta:+.4f}")

    best = max(ALGORITHMS, key=lambda a: getattr(result, a).ndcg_at_5)
    print(f"\nBest algorithm by NDCG@5: {best}")
