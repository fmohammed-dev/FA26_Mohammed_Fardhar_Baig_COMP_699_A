"""Measure how field and preference terms affect the existing candidate rankings."""

import csv
import json
from collections import defaultdict
from math import isclose, isfinite, log2
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "results/week_2"
OUT = ROOT / "results/week_3"
FEATURES = ("skill_coverage", "field_match", "preference_match")


def read_rows(name):
    with (BASELINE / name).open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def write_rows(name, rows):
    with (OUT / name).open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def dcg(grades):
    return sum((2**grade - 1) / log2(i + 2) for i, grade in enumerate(grades))


def run():
    protocol = json.loads((ROOT / "src/protocol.json").read_text())
    k, threshold = protocol["k"], protocol["relevance_threshold"]
    skills, field, preference = (protocol[key] for key in ("skill_weight", "field_weight", "preference_weight"))
    if (k, threshold, protocol["ndcg_gain"]) != (3, 1, "2**grade - 1"):
        raise ValueError("Expected the frozen Week 2 metric settings")
    weights = {
        "skill_only": (1, 0, 0),
        "structured": (skills, field, preference),
        "without_field": (skills, 0, preference),
        "without_preference": (skills, field, 0),
    }
    labels = defaultdict(dict)
    for row in json.loads((ROOT / "data/synthetic/relevance.json").read_text()):
        group = labels[row["student_id"]]
        oid, grade = row["opportunity_id"], row["grade"]
        if oid in group or grade not in (0, 1, 2):
            raise ValueError(f"Invalid relevance row: {row}")
        group[oid] = grade
    candidates = defaultdict(dict)
    for row in read_rows("score_components.csv"):
        group = candidates[row["student_id"]]
        oid = row["opportunity_id"]
        values = tuple(float(row[name]) for name in FEATURES)
        if oid in group or not all(isfinite(v) and 0 <= v <= 1 for v in values):
            raise ValueError(f"Duplicate or invalid score components: {row}")
        group[oid] = values
    if candidates.keys() != labels.keys() or any(candidates[s].keys() != labels[s].keys() for s in labels):
        raise ValueError("The score components and relevance labels cover different pairs")

    original = defaultdict(list)
    for row in read_rows("rankings.csv"):
        original[row["student_id"], row["method"]].append(row)
    baseline_metrics = {(r["student_id"], r["method"]): r for r in read_rows("metrics_by_student.csv")}
    by_student, top_three = [], []
    for student, group in sorted(candidates.items()):
        grades = labels[student]
        ideal = dcg(sorted(grades.values(), reverse=True)[:k])
        for method, w in weights.items():
            scores = {oid: sum(v * weight for v, weight in zip(values, w))
                      for oid, values in group.items()}
            ranking = sorted(group, key=lambda oid: (-scores[oid], oid))
            top_grades = [grades[oid] for oid in ranking[:k]]
            precision = sum(g >= threshold for g in top_grades) / k
            ndcg = dcg(top_grades) / ideal if ideal else 0.0
            if method in ("skill_only", "structured"):
                published = sorted(original[student, method], key=lambda r: int(r["rank"]))
                if ranking != [r["opportunity_id"] for r in published] or any(
                    not isclose(scores[r["opportunity_id"]], float(r["score"]), rel_tol=0, abs_tol=1e-12)
                    or grades[r["opportunity_id"]] != int(r["grade"]) for r in published
                ):
                    raise ValueError(f"Baseline ranking, score or grade differs: {student}, {method}")
                expected = baseline_metrics[student, method]
                if not all(isclose(a, float(expected[b]), rel_tol=0, abs_tol=1e-12)
                           for a, b in ((precision, "precision_at_3"), (ndcg, "ndcg_at_3"))):
                    raise ValueError(f"Baseline metrics differ: {student}, {method}")
            by_student.append(dict(student_id=student, method=method, precision_at_3=precision, ndcg_at_3=ndcg))
            for rank, oid in enumerate(ranking[:k], 1):
                top_three.append(dict(student_id=student, method=method, rank=rank,
                                      opportunity_id=oid, grade=grades[oid], score=scores[oid]))
    macro = []
    for method in weights:
        group = [r for r in by_student if r["method"] == method]
        macro.append(dict(method=method, profiles=len(group),
                          precision_at_3=mean(r["precision_at_3"] for r in group),
                          ndcg_at_3=mean(r["ndcg_at_3"] for r in group)))
    OUT.mkdir(parents=True, exist_ok=True)
    write_rows("ablation_by_student.csv", by_student)
    write_rows("ablation_macro.csv", macro)
    write_rows("ablation_top3.csv", top_three)
    print(f"Checked {sum(map(len, labels.values()))} labeled pairs and reproduced both Week 2 references.")


if __name__ == "__main__":
    run()
