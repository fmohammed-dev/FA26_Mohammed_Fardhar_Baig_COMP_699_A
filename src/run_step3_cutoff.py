"""Reproduce cutoff metrics and audit saved ranking transitions."""
import csv
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def metrics(grades, k):
    if not 0 < k <= len(grades) or any(g not in (0,1,2) for g in grades):
        raise ValueError("Invalid cutoff or grades")
    hits = sum(g > 0 for g in grades[:k])
    relevant = sum(g > 0 for g in grades)
    def dcg(gs):
        return sum((2**g-1)/math.log2(i+2) for i,g in enumerate(gs[:k]))
    ideal = dcg(sorted(grades, reverse=True))
    return hits/k, hits/relevant if relevant else 0, dcg(grades)/ideal if ideal else 0

def read(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))

def analyze(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[row["student_id"],row["method"]].append(row)
    results = []
    for (student,method), group in groups.items():
        group.sort(key=lambda r:int(r["rank"]))
        if [int(r["rank"]) for r in group] != list(range(1,len(group)+1)) or len({r["opportunity_id"] for r in group}) != len(group):
            raise ValueError("Invalid ranking")
        grades = [int(r["grade"]) for r in group]
        for k in (1,3,5):
            results.append((student,method,k,*metrics(grades,k)))
    return groups, results

def main():
    groups, results = analyze(read(ROOT/"results/week_2/rankings.csv"))
    expected = read(ROOT/"results/step_3/cutoff_by_profile.csv")
    actual = {(s,m,k):(p,r,n) for s,m,k,p,r,n in results}
    assert len(actual)==len(expected)
    for row in expected:
        values = actual[row["student_id"],row["method"],int(row["k"])]
        assert all(abs(a-float(row[b]))<1e-8 for a,b in zip(values,("precision","recall","ndcg")))
    for row in read(ROOT/"results/step_3/cutoff_summary.csv"):
        selected=[v for (s,m,k),v in actual.items() if m==row["method"] and k==int(row["k"])]
        assert all(abs(sum(v[i] for v in selected)/len(selected)-float(row[b]))<1e-8 for i,b in enumerate(("precision","recall","ndcg")))
    for row in read(ROOT/"results/week_2/metrics_by_student.csv"):
        p,_,n=actual[row["student_id"],row["method"],3]
        assert abs(p-float(row["precision_at_3"]))<1e-8 and abs(n-float(row["ndcg_at_3"]))<1e-8
    for student in sorted({s for s,m in groups}):
        a,b=(groups[student,m] for m in ("skill_only","structured"))
        assert {r["opportunity_id"]:r["grade"] for r in a}=={r["opportunity_id"]:r["grade"] for r in b}
        old,new=({r["opportunity_id"] for r in g[:3]} for g in (a,b))
        failures=sorted({r["opportunity_id"] for r in a[:3]+b[:3] if int(r["grade"])==0})
        print(student,"removed",sorted(old-new),"added",sorted(new-old),"grade-zero",failures)
    print("Cutoff tables and original K=3 metrics verified")

if __name__=="__main__":
    main()
