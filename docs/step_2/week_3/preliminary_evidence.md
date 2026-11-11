# Preliminary Evidence

**Graduate Career Opportunity Recommender**

## 1. Research question and hypothesis

For fixed synthetic graduate-student scenarios, does combining skill coverage, academic field, and stated preferences improve top-three recommendations over skill coverage alone? Extra compatibility signals may improve ordering when skills alone leave ties or favor weak contextual matches.

## 2. Preliminary analysis

The component-removal analysis compares the full structured score with the skill-only reference and two conditions that remove either academic-field compatibility or preferences. It measures how each term contributes to ranking on the existing benchmark.

## 3. Inputs, parameters, and metrics

Inputs are 6 fictional profiles, 12 fictional opportunities, and 72 author-graded pairs. The analysis uses saved skill, field and preference scores from score_components.csv. Remaining weights stay fixed when a term is removed. Preferences combine opportunity type and work mode equally. Ties use ascending opportunity ID.

Grade 1 or 2 counts as relevant for Precision@3. NDCG@3 uses gains of 2^grade - 1, discounted by log2(rank + 1) and normalized against the ideal ranking for the same profile. Macro values weight all six profiles equally.

## 4. Preliminary evidence

| Condition | Skills weight | Field weight | Preference weight | Precision@3 | NDCG@3 |
| --- | --- | --- | --- | --- | --- |
| Skills only | 1.00 | 0.00 | 0.00 | 0.8333 | 0.8396 |
| Full structured | 0.60 | 0.25 | 0.15 | 0.8333 | 0.9395 |
| Without field | 0.60 | 0.00 | 0.15 | 0.8333 | 0.9342 |
| Without preference | 0.60 | 0.25 | 0.00 | 0.8333 | 0.8501 |

Source: ablation_macro.csv. The per-profile NDCG@3 values are shown on the next page.

## 5. Evidence and interpretation

| Profile | Skills only | Full structured | Without field | Without preference |
| --- | --- | --- | --- | --- |
| S01 | 0.8790 | 1.0000 | 1.0000 | 1.0000 |
| S02 | 0.8213 | 0.8790 | 0.8790 | 0.7003 |
| S03 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| S04 | 0.7003 | 0.8790 | 0.8790 | 0.7003 |
| S05 | 0.8790 | 0.8790 | 0.8473 | 0.8790 |
| S06 | 0.7579 | 1.0000 | 1.0000 | 0.8213 |

Source: ablation_by_student.csv. Candidate IDs, grades, ranks, and scores are in ablation_top3.csv.

The full structured score has the highest macro NDCG@3 (0.9395). Removing preferences lowers it to 0.8501, with decreases for S02, S04, and S06. Removing the field term lowers it to 0.9342, with a decrease for S05. All conditions have macro Precision@3 of 0.8333. In these scenarios the preference term mainly affects ordering quality.

## 6. Validity and reproducibility

The script checks that all 72 score-component rows have valid values and corresponding grades. It reproduces the two Week 2 ranking orders, scores, grades and per-profile metrics before writing new results. Run python src/run_week3_evidence.py with Python 3.12. The script uses the standard library and the saved score components.

The grades reward contextual fit and therefore share concepts with the score. The benchmark is small, synthetic, and author-graded. A term-removal effect can reflect the interaction with other terms or tie-breaking, so the measured changes do not isolate the independent value of each attribute in real advising.

## 7. Research design revision

Keep both ablation conditions as diagnostic references. Distinguish hard eligibility rules from preferences in the next benchmark. Narrow the current claim to better ordering on these constructed scenarios, with the stronger observed sensitivity to the preference term.

## 8. Prioritized next research tasks

1. Add profiles with conflicting preferences and transferable academic backgrounds.

2. Label eligibility separately from preference and obtain independent grades.

3. Freeze distinct development and evaluation profiles before tuning.

4. Compare a hard-eligibility filter with soft scoring on the held-out profiles.
