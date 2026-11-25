# Profile-level transitions and recommendation failure audit

## Task 1 — Profile-level comparison

The frozen Week 2 rankings were compared at K=3. The top-three membership changes for S01, S02 and S03; S04 and S06 change order only; S05 is unchanged.

| Profile | Precision@3 change | NDCG@3 change | Interpretation |
| --- | ---: | ---: | --- |
| S01 | +0.333333 | +0.121038 | Relevant O09 replaces irrelevant O03 |
| S02 | -0.333333 | +0.057648 | Grade-2 O04 moves first, but irrelevant O02 replaces relevant O01 |
| S03 | 0 | 0 | Grade-1 O05 replaces grade-1 O12 |
| S04 | 0 | +0.178686 | Grade-2 O08 moves first |
| S05 | 0 | 0 | Identical top three |
| S06 | 0 | +0.242076 | Grade-2 O12 moves from third to first |

Four profiles improve NDCG@3 and two remain unchanged. Precision gains and losses cancel across profiles. The two metrics therefore describe different aspects of ranking quality.

## Task 2 — Failure analysis

The union of grade-zero top-three pairs across both methods contains four pairs. The structured method removes S01/O03 (rank 3 to 5), introduces S02/O02 (rank 4 to 3), and retains S04/O02 and S05/O12 at rank 3.

The fixed score is 0.60 times skill coverage plus 0.25 times field match plus 0.15 times preference match.

- S02/O02: 0.300 + 0.250 + 0.075 = 0.625, exceeding the displaced grade-1 O01 score of 0.300. Field and preference bonuses favor the grade-zero candidate.
- S04/O02: 0.300 + 0 + 0.075 = 0.375, exceeding grade-1 O03 at 0.300. Both have half skill coverage and no field match; the preference term separates them.
- S05/O12: 0.600 + 0 + 0.075 = 0.675, exceeding grade-1 O01 and O05 at 0.450 each. Full skill coverage offsets the missing field match. The finance opportunity remains a poor domain fit under the constructed labels.
- S01/O03: 0.300 + 0 + 0.075 = 0.375; grade-1 O09 scores 0.700 and replaces it.

These are arithmetic explanations of saved scores, not independent evidence that the author-defined relevance grades are correct. No scoring rule, dataset, or eligibility constraint was changed.

## Evidence and reproduction

Inputs: results/week_2/rankings.csv, score_components.csv, metrics_by_student.csv and data/synthetic/relevance.json. For each profile, compare the ordered top-three IDs, subtract the skill-only metrics from structured metrics, and identify grade-zero pairs in either top three. For each such pair, multiply the saved components by the fixed weights and identify the highest-ranked relevant candidate outside the structured top three. Ties follow the committed ranking order. The resulting tables are results/step_3/profile_top3_transitions.csv and results/step_3/top3_component_failure_audit.csv. The tables were calculated directly from the saved inputs; no fresh model execution or separate validation suite was performed.

Tasks 3–5 remain outside this update.
