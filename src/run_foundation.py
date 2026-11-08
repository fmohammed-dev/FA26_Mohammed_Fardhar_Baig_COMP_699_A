"""Week 1: input validation and descriptive evidence, without comparative results."""

from pathlib import Path
import json
import hashlib
import platform
import importlib.metadata
import pandas as pd
from career_methods import validate_inputs

ROOT = Path(__file__).resolve().parents[1]


def run():
    """Validate the fixed inputs and save the Week 1 descriptive evidence."""
    input_dir = ROOT / "data/synthetic"
    output_dir = ROOT / "results/week_1"
    output_dir.mkdir(parents=True, exist_ok=True)
    profiles = json.loads((input_dir / "profiles.json").read_text())
    opportunities = json.loads((input_dir / "opportunities.json").read_text())
    labels = json.loads((input_dir / "relevance.json").read_text())
    manifest = json.loads((input_dir / "manifest.json").read_text())
    for filename, expected_hash in manifest["sha256"].items():
        if (
            hashlib.sha256((input_dir / filename).read_bytes()).hexdigest()
            != expected_hash
        ):
            raise ValueError("Frozen input changed: " + filename)
    checks = validate_inputs(profiles, opportunities, labels)
    checks["input_digests_match"] = True
    pd.DataFrame(
        [{"check": name, "passed": passed} for name, passed in checks.items()]
    ).to_csv(output_dir / "validation_checks.csv", index=False)
    pd.DataFrame(
        [
            {
                "student_id": profile["student_id"],
                "field": profile["field"],
                "skills": len(profile["skills"]),
                "preferred_type": profile["preferred_type"],
                "preferred_modes": "|".join(profile["preferred_modes"]),
            }
            for profile in profiles
        ]
    ).to_csv(output_dir / "profile_summary.csv", index=False)
    pd.DataFrame(
        [
            {
                "opportunity_id": opportunity["opportunity_id"],
                "title": opportunity["title"],
                "required_skills": "|".join(opportunity["required_skills"]),
                "accepted_fields": "|".join(opportunity["accepted_fields"]),
                "type": opportunity["type"],
                "mode": opportunity["mode"],
            }
            for opportunity in opportunities
        ]
    ).to_csv(output_dir / "opportunity_summary.csv", index=False)
    pd.DataFrame(labels).groupby(["student_id", "grade"]).size().unstack(
        fill_value=0
    ).to_csv(output_dir / "grade_distribution.csv")
    summary = {
        "profiles": len(profiles),
        "opportunities": len(opportunities),
        "pairs": len(labels),
        "fields": len({profile["field"] for profile in profiles}),
        "checks_passed": len(checks),
        "comparative_experiment_executed": False,
        "python": platform.python_version(),
        "packages": {
            package: importlib.metadata.version(package)
            for package in ["numpy", "pandas"]
        },
        "input_hashes": manifest["sha256"],
    }
    (output_dir / "execution_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    run()
