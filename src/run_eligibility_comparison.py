"""Priority 4: hypothetical strict preference constraints versus soft structured ranking.

Research-only synthetic experiment. Type/mode restrictions are imposed for this
experiment; they are NOT verified employer eligibility requirements.
"""
import csv
import json
import math
from pathlib import Path

from career_methods import components, structured_score, ordered

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "data" / "extension_1"
OUT = ROOT / "results" / "priority_4"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def dcg(grades):
    return sum((2 ** grade - 1) / math.log2(i + 2) for i, grade in enumerate(grades[:3]))


def metrics(ranked, all_candidates):
    """Fixed-denominator P@3 and full-catalog ideal NDCG@3; zero-fill short lists.

    Full-catalog ideal is shared across methods, so filtering is penalized when
    it removes relevant opportunities. Coverage is reported separately.
    """
    selected = [row["grade"] for row in ranked[:3]]
    ideal = dcg(sorted((row["grade"] for row in all_candidates), reverse=True))
    return (sum(g >= 1 for g in selected) / 3,
            dcg(selected) / ideal if ideal else 0.0)


def write_csv(name, rows, columns):
    with (OUT / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def run():
    profiles = load_json(EXT / "profiles.json")
    opportunities = load_json(ROOT / "data/synthetic/opportunities.json")
    labels = load_json(EXT / "labels.json")
    split = load_json(EXT / "split.json")
    protocol = load_json(ROOT / "src/protocol.json")
    assert len(profiles) == 6 and len(opportunities) == 12 and len(labels) == 72
    assert set(split["development"]).isdisjoint(split["evaluation"])
    assert set(split["development"] + split["evaluation"]) == {
        p["student_id"] for p in profiles
    }
    assert len({(r["student_id"], r["opportunity_id"]) for r in labels}) == 72
    assert all(r["review_status"] == "author_provisional"
               and r["eligibility_status"] == "not_assessed" for r in labels)
    grades = {(r["student_id"], r["opportunity_id"]): r["relevance_grade"]
              for r in labels}
    annotations = {(r["student_id"], r["opportunity_id"]): r for r in labels}
    results, rankings = [], []
    for profile in profiles:
        sid = profile["student_id"]
        partition = "development" if sid in split["development"] else "evaluation"
        candidates = []
        for opportunity in opportunities:
            oid = opportunity["opportunity_id"]
            parts = components(profile, opportunity)
            type_match = profile["preferred_type"] == opportunity["type"]
            mode_match = opportunity["mode"] in profile["preferred_modes"]
            label = annotations[sid, oid]
            assert label["preference_type_match"] == type_match
            assert label["preference_mode_match"] == mode_match
            candidates.append({
                "student_id": sid, "opportunity_id": oid,
                "structured": structured_score(parts, protocol),
                "grade": grades[sid, oid],
                "passes_hypothetical_constraints": type_match and mode_match,
            })
        for method in ("soft_structured", "strict_preference_filter"):
            eligible = (candidates if method == "soft_structured" else
                        [r for r in candidates if r["passes_hypothetical_constraints"]])
            ranked = ordered(eligible, "structured")
            p3, n3 = metrics(ranked, candidates)
            results.append({
                "student_id": sid, "split": partition, "method": method,
                "candidate_count": len(ranked), "top3_count": min(3, len(ranked)),
                "top3_coverage": min(3, len(ranked)) / 3,
                "precision_at_3_zero_fill": p3,
                "ndcg_at_3_full_catalog_ideal": n3,
            })
            for i, row in enumerate(ranked, 1):
                rankings.append({
                    "student_id": sid, "split": partition, "method": method,
                    "rank": i, "opportunity_id": row["opportunity_id"],
                    "score": f'{row["structured"]:.6f}', "grade": row["grade"],
                })
    columns = ["student_id", "split", "method", "candidate_count", "top3_count",
               "top3_coverage", "precision_at_3_zero_fill",
               "ndcg_at_3_full_catalog_ideal"]
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv("metrics_by_profile.csv", results, columns)
    write_csv("rankings.csv", rankings,
              ["student_id", "split", "method", "rank", "opportunity_id",
               "score", "grade"])
    macro = []
    for partition in ("development", "evaluation"):
        for method in ("soft_structured", "strict_preference_filter"):
            subset = [r for r in results if r["split"] == partition and
                      r["method"] == method]
            macro.append({
                "split": partition, "method": method, "profiles": len(subset),
                "mean_candidates": sum(r["candidate_count"] for r in subset) / len(subset),
                "mean_top3_coverage": sum(r["top3_coverage"] for r in subset) / len(subset),
                "mean_precision_at_3_zero_fill": sum(
                    r["precision_at_3_zero_fill"] for r in subset) / len(subset),
                "mean_ndcg_at_3_full_catalog_ideal": sum(
                    r["ndcg_at_3_full_catalog_ideal"] for r in subset) / len(subset),
            })
    write_csv("metrics_summary.csv", macro,
              ["split", "method", "profiles", "mean_candidates",
               "mean_top3_coverage", "mean_precision_at_3_zero_fill",
               "mean_ndcg_at_3_full_catalog_ideal"])
    assert len(results) == 12 and len(rankings) <= 144
    print("Validated 72 provisional annotations; wrote 3 result CSVs.")
    for row in macro:
        print(row)


if __name__ == "__main__":
    run()
