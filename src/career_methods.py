"""Inspectable structured matching; labels never enter the scoring functions."""

import math


def normalize(values):
    """Trim, lowercase and deduplicate skill or field names."""
    return {
        value.strip().lower()
        for value in values
        if isinstance(value, str) and value.strip()
    }


def components(profile, opportunity):
    """Calculate the existing skill, field and preference match components."""
    required_skills = normalize(opportunity["required_skills"])
    if not required_skills:
        raise ValueError("At least one required skill is needed")

    skill_coverage = len(normalize(profile["skills"]) & required_skills) / len(
        required_skills
    )
    field_match = float(
        profile["field"].strip().lower() in normalize(opportunity["accepted_fields"])
    )
    type_match = float(profile["preferred_type"] == opportunity["type"])
    mode_match = float(opportunity["mode"] in profile["preferred_modes"])
    return {
        "skill_coverage": skill_coverage,
        "field_match": field_match,
        "type_match": type_match,
        "mode_match": mode_match,
        "preference_match": (type_match + mode_match) / 2,
    }


def structured_score(parts, protocol):
    """Combine the three components using the predeclared weights."""
    weights = [
        protocol[key] for key in ["skill_weight", "field_weight", "preference_weight"]
    ]
    if any(weight < 0 for weight in weights) or not math.isclose(sum(weights), 1):
        raise ValueError("Weights must be nonnegative and sum to one")
    return (
        weights[0] * parts["skill_coverage"]
        + weights[1] * parts["field_match"]
        + weights[2] * parts["preference_match"]
    )


def ordered(rows, score):
    """Sort by descending score, resolving ties by opportunity ID."""
    return sorted(rows, key=lambda row: (-row[score], row["opportunity_id"]))


def precision_at_k(grades, k):
    """Measure the relevant fraction of the first k graded candidates."""
    if k < 1 or len(grades) < k:
        raise ValueError("Invalid k")
    return sum(grade >= 1 for grade in grades[:k]) / k


def ndcg_at_k(grades, k):
    """Normalize discounted exponential gains against the ideal ordering."""
    if k < 1 or len(grades) < k:
        raise ValueError("Invalid k")

    def discounted_gain(ordered_grades):
        return sum(
            (2**grade - 1) / math.log2(index + 2)
            for index, grade in enumerate(ordered_grades[:k])
        )

    ideal_gain = discounted_gain(sorted(grades, reverse=True))
    return discounted_gain(grades) / ideal_gain if ideal_gain else 0.0


def _require_records(records, name):
    """Reject empty collections and non-object rows before indexing fields."""
    if not isinstance(records, list) or not records:
        raise ValueError(f"{name} must be a nonempty list of objects")
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"{name}[{index}] must be an object")


def _require_text(record, field, location):
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{location}.{field} must be a nonempty string")


def _require_text_list(record, field, location, allow_empty=False):
    """Validate list types without silently dropping malformed entries."""
    values = record.get(field)
    if not isinstance(values, list) or (not allow_empty and not values):
        qualifier = "a list" if allow_empty else "a nonempty list"
        raise ValueError(f"{location}.{field} must be {qualifier} of nonempty strings")
    if any(not isinstance(value, str) or not value.strip() for value in values):
        raise ValueError(f"{location}.{field} must contain only nonempty strings")


def validate_inputs(profiles, opportunities, labels):
    """Validate schema first, then identifier, pair-grid and relevance integrity.

    Empty profile skill lists are valid. Required opportunity skills, accepted
    fields and preferred work modes must be nonempty lists. Successful calls
    retain the original check names so existing evidence tables stay comparable.
    """
    for records, name in [
        (profiles, "profiles"),
        (opportunities, "opportunities"),
        (labels, "labels"),
    ]:
        _require_records(records, name)

    for index, profile in enumerate(profiles):
        location = f"profiles[{index}]"
        for field in ["student_id", "field", "preferred_type"]:
            _require_text(profile, field, location)
        _require_text_list(profile, "skills", location, allow_empty=True)
        _require_text_list(profile, "preferred_modes", location)

    for index, opportunity in enumerate(opportunities):
        location = f"opportunities[{index}]"
        for field in ["opportunity_id", "title", "type", "mode"]:
            _require_text(opportunity, field, location)
        _require_text_list(opportunity, "required_skills", location)
        _require_text_list(opportunity, "accepted_fields", location)

    for index, label in enumerate(labels):
        location = f"labels[{index}]"
        for field in ["student_id", "opportunity_id", "rationale"]:
            _require_text(label, field, location)

    student_ids = {profile["student_id"] for profile in profiles}
    opportunity_ids = {opportunity["opportunity_id"] for opportunity in opportunities}
    labeled_pairs = [(label["student_id"], label["opportunity_id"]) for label in labels]
    expected_pairs = {
        (student_id, opportunity_id)
        for student_id in student_ids
        for opportunity_id in opportunity_ids
    }
    checks = {
        "unique_student_ids": len(student_ids) == len(profiles),
        "unique_opportunity_ids": len(opportunity_ids) == len(opportunities),
        "unique_labeled_pairs": len(set(labeled_pairs)) == len(labeled_pairs),
        "complete_pair_grid": set(labeled_pairs) == expected_pairs,
        "valid_relevance_grades": all(
            type(label.get("grade")) is int and label["grade"] in {0, 1, 2}
            for label in labels
        ),
        "required_profile_fields": True,
        "required_opportunity_fields": True,
        "pair_rationales_present": True,
    }
    failed_checks = [name for name, passed in checks.items() if not passed]
    if failed_checks:
        raise ValueError("Input integrity checks failed: " + ", ".join(failed_checks))
    return checks
