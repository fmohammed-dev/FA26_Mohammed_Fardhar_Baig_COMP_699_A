# Graduate Career Opportunity Recommender

This project investigates transparent ranking of career opportunities for graduate-student profiles using structured attributes. The current implementation uses synthetic scenarios and fixed arithmetic rather than a trained model.

## Research question
For fixed synthetic graduate-student scenarios, does combining skill coverage, academic-field compatibility and stated career preferences improve Precision@3 and NDCG@3 over skill-only ranking?

Additional compatibility attributes may improve ordering in some cases, but improvement is not assumed across every profile or metric. The experiment measures diagnostic ranking behavior, not placement outcomes or real student utility.

## Completed milestone work

### Week 1 - Research foundation
- Created 6 fictional graduate profiles, 12 fictional opportunities and all 72 graded pairs.
- Recorded per-pair rationale and fixed input hashes before scoring.
- Executed 9 input-integrity checks and saved descriptive tables.
- Prepared `docs/step_2/week_1/research_foundation.pdf`.

### Week 2 - Method and baseline
- Implemented a skill-coverage reference and a fixed structured score: 0.60 skills + 0.25 academic field + 0.15 preferences.
- Used identical candidates, opportunity-ID tie-breaking, K=3 and fixed relevance grades for both methods.
- Executed 14 known-example method tests and 13 input/numerical checks; all passed.
- Saved score components, complete rankings, per-profile/macro metrics, failure cases and repeatability evidence.
- Prepared `docs/step_2/week_2/method_and_baseline.pdf`.

| Method | Macro Precision@3 | Macro NDCG@3 |
|---|---:|---:|
| Skill only | 0.833333 | 0.839573 |
| Structured score | 0.833333 | 0.939481 |

Average NDCG@3 improves by 0.099908 while Precision@3 is unchanged. S01 gains a relevant top-three result, whereas S02 loses one. S05 retains an irrelevant finance opportunity despite a domain mismatch. These failures and the author-defined nature of the labels limit any claim of general effectiveness.

## Reproduce the work
Use Python 3.12 with a dedicated environment. Run these separate commands from the repository root:
```bash
python -m pip install -r src/requirements.txt
python src/prepare_inputs.py
python src/run_foundation.py
python -m unittest discover -s src -p 'test_*.py' -v
python src/run_comparison.py
python src/build_reports.py
```
Alternatively open `src/career_opportunity_recommender.ipynb` from the root or src folder, select the environment containing these packages and run all cells. Jupyter/ipykernel can be installed separately for the notebook interface. The notebook includes the actual input construction and scoring/evaluation code, not only links to scripts.

No API credentials, live student records or external dataset downloads are required. Generation is deterministic and recreates the fixed input files. The comparison verifies their hashes; changing inputs requires an explicitly revised manifest and documented design change. Generated output files are overwritten on rerun. Repeated comparison runs produced identical ranking/metric CSVs.

## Repository structure
- `src/`: input generator, reusable method, two experiment entry points, tests, fixed protocol, executed notebook, dependencies and report generator.
- `data/synthetic/`: profile/opportunity JSON, relevance grades with rationales, and input manifest.
- `results/week_1/`: descriptive tables, validation checks and foundation execution record.
- `results/week_2/`: full scores/rankings, metrics, top-three cases, tests, plot and repeatability evidence.
- `docs/step_2/week_1/`: required foundation PDF and editable Markdown.
- `docs/step_2/week_2/`: required method/baseline PDF and editable Markdown.
- `docs/references/`: supplied bibliography and selected-paper record.

## Interpretation and next work
The data are author-constructed and the judgments are not independent. Although grades were specified before scoring, they share concepts with the scoring rule; apparent improvements may partly reflect scenario design. There is no train/test split, learned weight, parameter tuning or statistical superiority claim. Soft preferences are not eligibility guarantees or universal requirements.

The selected Jobindex paper concerns candidate recommendations for recruiters. It provides related context; this code neither reproduces that system nor measures recruiter interaction. Future work will expand scenarios, strengthen independent relevance judgments, separate development and evaluation before tuning, and examine hard versus soft constraints. Week 3 and the final combined submission remain pending.

The two completed milestone sections were prepared during the current work session. Their numbering describes assignment scope, not backdated implementation or commit history.
