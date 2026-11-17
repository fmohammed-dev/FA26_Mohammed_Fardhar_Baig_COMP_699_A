# Priority 4: hypothetical constraint filtering versus soft structured ranking

## Scope and methods
Research-only comparison on extension 1: 6 fictional profiles, 12 original fictional opportunities, 72 author-provisional relevance judgments. Original Step 2 benchmark and scoring weights (0.60 skills, 0.25 field, 0.15 preferences) are unchanged.

**Soft structured:** rank all 12 opportunities by the original score. **Strict hypothetical preference filter:** retain only opportunities whose employment type equals the profile's preferred type AND whose mode belongs to its preferred modes; rank survivors by the identical score. These imposed conditions are **not verified job eligibility rules**. Academic field is never a mandatory exclusion. No real hiring eligibility or student authorization is inferred.

## Evaluation definitions
At K=3, short filtered lists are **zero-filled** for Precision@3 (relevant items / 3) and NDCG@3 uses the same full 12-opportunity ideal for both methods, rather than an easier filtered-catalog ideal. Candidate count and top-three coverage (min(3, candidates)/3) are reported separately. This fixed-denominator convention differs from the earlier exploratory comparison where short-list metrics were undefined.

## Macro results
| Split | Method | Mean candidates | Mean top-three coverage | Precision@3 (zero-fill) | NDCG@3 (full-catalog ideal) |
|---|---|---:|---:|---:|---:|
| Development (S07-S09) | Soft structured | 12.00 | 1.0000 | 0.8889 | 0.9056 |
| Development (S07-S09) | Strict preference filter | 3.00 | 0.8889 | 0.6667 | 0.6006 |
| Evaluation (S10-S12) | Soft structured | 12.00 | 1.0000 | 1.0000 | 1.0000 |
| Evaluation (S10-S12) | Strict preference filter | 1.00 | 0.3333 | 0.0000 | 0.0000 |

Filtered candidate counts by profile: development S07=2, S08=4, S09=3; evaluation S10=2, S11=1, S12=0. The zero scores for strict filtering on evaluation profiles reflect no relevant candidates surviving the hypothetical rules, not proof of poor real-world eligibility decisions.

## Interpretation and limitations
Under the imposed preference-as-constraint scenario, strict filtering sharply reduced coverage and removed author-labeled relevant opportunities. This is an illustrative **sensitivity test**, not evidence that real mandatory eligibility rules should be ignored. The three evaluation profiles were preassigned, but this experiment's preliminary candidate counts were inspected before documentation; do not describe this as an untouched blind evaluation. The same opportunity catalog is shared across partitions. Grades are synthetic, provisional and author-assigned, and no independent annotation review has occurred. No statistical generalization or real student placement claim is warranted.

## Reproducibility and next work
Run `python src/run_eligibility_comparison.py` from the repository root (Python standard library and existing `src/career_methods.py`). Outputs: `results/priority_4/metrics_by_profile.csv`, `rankings.csv`, and `metrics_summary.csv`. The comparison uses explicit validation checks for profile split, label grid, and preference-compatibility annotations. The recorded CSVs were calculated from the same declared formulas and inputs; a separate execution log has not been independently verified.

Next: independently review labels; specify and document genuine mandatory eligibility data if available; investigate filtered-list abstention and coverage-aware alternatives without tuning against evaluation cases.
