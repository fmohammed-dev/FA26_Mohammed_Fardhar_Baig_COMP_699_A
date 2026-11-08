"""Week 2: compare fixed structured scoring with a skill-only reference."""

from pathlib import Path
import json
import hashlib
import platform
import importlib.metadata
import math
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from career_methods import (
    validate_inputs,
    components,
    structured_score,
    ordered,
    precision_at_k,
    ndcg_at_k,
)

ROOT = Path(__file__).resolve().parents[1]


def run():
    """Run both fixed rankers and save the Week 2 comparison evidence."""
    input_dir = ROOT / "data/synthetic"
    output_dir = ROOT / "results/week_2"
    output_dir.mkdir(parents=True, exist_ok=True)
    protocol_bytes = (ROOT / "src/protocol.json").read_bytes()
    protocol = json.loads(protocol_bytes)
    profiles = json.loads((input_dir / "profiles.json").read_text())
    opportunities = json.loads((input_dir / "opportunities.json").read_text())
    labels = json.loads((input_dir / "relevance.json").read_text())
    manifest = json.loads((input_dir / "manifest.json").read_text())
    for name, expected_hash in manifest["sha256"].items():
        if hashlib.sha256((input_dir / name).read_bytes()).hexdigest() != expected_hash:
            raise ValueError("Frozen input changed: " + name)
    checks = validate_inputs(profiles, opportunities, labels)
    checks["input_digests_match"] = True
    grades = {
        (label["student_id"], label["opportunity_id"]): label["grade"]
        for label in labels
    }
    scores = []
    ranks = []
    metric_rows = []
    for profile in profiles:
        candidates = []
        for opportunity in opportunities:
            parts = components(profile, opportunity)
            candidates.append(
                {
                    "student_id": profile["student_id"],
                    "opportunity_id": opportunity["opportunity_id"],
                    **parts,
                    "skill_only": parts["skill_coverage"],
                    "structured": structured_score(parts, protocol),
                }
            )
        scores.extend(candidates)
        for method in ["skill_only", "structured"]:
            ranked = ordered(candidates, method)
            ranked_grades = [
                grades[profile["student_id"], candidate["opportunity_id"]]
                for candidate in ranked
            ]
            for rank, candidate in enumerate(ranked, 1):
                ranks.append(
                    {
                        "student_id": profile["student_id"],
                        "method": method,
                        "opportunity_id": candidate["opportunity_id"],
                        "rank": rank,
                        "score": candidate[method],
                        "grade": ranked_grades[rank - 1],
                    }
                )
            metric_rows.append(
                {
                    "student_id": profile["student_id"],
                    "method": method,
                    "precision_at_3": precision_at_k(ranked_grades, protocol["k"]),
                    "ndcg_at_3": ndcg_at_k(ranked_grades, protocol["k"]),
                }
            )
    score_table = pd.DataFrame(scores)
    ranking_table = pd.DataFrame(ranks)
    metrics = pd.DataFrame(metric_rows)
    aggregate = (
        metrics.groupby("method")[["precision_at_3", "ndcg_at_3"]].mean().reset_index()
    )
    checks["all_scores_finite_and_bounded"] = bool(
        score_table[["skill_only", "structured"]]
        .map(lambda value: math.isfinite(value) and 0 <= value <= 1)
        .all()
        .all()
    )
    checks["two_full_rankings_per_profile"] = len(ranks) == 2 * len(labels)
    checks["grades_unchanged_during_execution"] = (
        hashlib.sha256((input_dir / "relevance.json").read_bytes()).hexdigest()
        == manifest["sha256"]["relevance.json"]
    )
    checks["protocol_unchanged_during_execution"] = (
        ROOT / "src/protocol.json"
    ).read_bytes() == protocol_bytes
    assert all(checks.values())
    for name, frame in [
        ("score_components", score_table),
        ("rankings", ranking_table),
        ("metrics_by_student", metrics),
        ("metrics_summary", aggregate),
    ]:
        frame.to_csv(output_dir / (name + ".csv"), index=False)
    pd.DataFrame(
        [{"check": name, "passed": passed} for name, passed in checks.items()]
    ).to_csv(output_dir / "validation_checks.csv", index=False)
    ranking_table[ranking_table["rank"] <= 3].to_csv(
        output_dir / "top3_recommendations.csv", index=False
    )
    paired = metrics.pivot(
        index="student_id", columns="method", values=["precision_at_3", "ndcg_at_3"]
    )
    paired.columns = ["_".join(column) for column in paired.columns]
    for metric in ["precision_at_3", "ndcg_at_3"]:
        paired[metric + "_delta"] = (
            paired[metric + "_structured"] - paired[metric + "_skill_only"]
        )
    paired.to_csv(output_dir / "paired_differences.csv")
    figure, axes = plt.subplots(figsize=(7, 3.6))
    ndcg_by_student = metrics.pivot(
        index="student_id", columns="method", values="ndcg_at_3"
    )
    ndcg_by_student.plot.bar(ax=axes, color=["#9AA8B5", "#235789"])
    axes.set_ylim(0, 1.05)
    axes.set(
        ylabel="NDCG@3",
        xlabel="Synthetic student scenario",
        title="Initial structured ranking comparison",
    )
    axes.legend(["Skill only", "Structured"], loc="lower right")
    figure.tight_layout()
    figure.savefig(output_dir / "ndcg_by_student.png", dpi=160)
    plt.close(figure)
    summary = {
        "python": platform.python_version(),
        "packages": {
            package: importlib.metadata.version(package)
            for package in ["numpy", "pandas", "matplotlib"]
        },
        "profiles": len(profiles),
        "opportunities": len(opportunities),
        "pairs": len(labels),
        "protocol": protocol,
        "protocol_sha256": hashlib.sha256(protocol_bytes).hexdigest(),
        "input_hashes": manifest["sha256"],
        "validation_checks_passed": len(checks),
        "training": "none",
        "randomness": "none",
        "independent_annotations": False,
    }
    (output_dir / "execution_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    print(aggregate.to_string(index=False))
    print("\nPer-scenario differences:\n" + paired.to_string())
    return aggregate


if __name__ == "__main__":
    run()
