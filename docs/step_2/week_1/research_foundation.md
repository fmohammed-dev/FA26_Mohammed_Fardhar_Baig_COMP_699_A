# Research Foundation

Graduate Career Opportunity Recommender | Mohammed Fardhar Baig

## 1. Research question and tentative answer

For fixed synthetic graduate-student scenarios, does a structured score combining skill coverage, academic-field compatibility and stated career preferences improve Precision@3 and NDCG@3 over skill-only ranking?

The working hypothesis is that academic-field and stated-preference compatibility may resolve some skill-only ties or unsuitable recommendations. Improvement is not assumed for every profile or metric. The broad proposal is operationalized as a small, transparent structured-ranking study; employment outcomes are outside the current evidence.

## 2. Evidence required

The intended evidence is a controlled comparison of two rankings over the same candidates and fixed relevance grades. Week 2 will calculate Precision@3 and NDCG@3 per student scenario, macro averages, paired differences and candidate-level failure cases. The Week 1 foundation produces input tables, grade distributions and integrity checks only. A dataset is a source; scores and evaluated ordering differences are computed evidence. Neither alone proves usefulness to actual students.

## 3. Research inputs and source context

The inputs are six synthetic graduate profiles and twelve fictional career opportunities, giving all 72 profile-opportunity pairs. Profiles cover data science, computer science, business analytics, cybersecurity, health informatics and finance. Attributes include canonical skills, academic field, desired opportunity type and work modes. Opportunities contain required skills, accepted fields, type and mode. No live vacancy data or real student information is used.

Every pair has a fixed grade and rationale. Grade 2 represents strong intended role fit, grade 1 partial or transferable fit or a material contextual limitation, and grade 0 no useful match in that scenario. Grades are explicitly authored before scoring and are not generated from the weighted formula. They are nevertheless based on related concepts, so evaluation is not independent of the scenario design. JSON input files and a SHA-256 manifest are saved under data/synthetic/.

The supplied bibliography provides recommender-system and job-recommendation context. The selected Kaya and Bogers Jobindex paper concerns candidate recommendations used by recruiters; this project ranks opportunities for student profiles. Its deployed method and interaction outcomes are not reproduced. The de Ruijt and Bhulai review highlights how data availability affects method choice and validation, motivating a modest diagnostic scope when interaction data are absent.

## 4. Environment and code organization

Executed environment: Python 3.12.14, NumPy 2.3.5 and pandas 2.2.3. src/requirements.txt pins the tested packages for both stages. Matplotlib supports the Week 2 plot and ReportLab renders the reports. Jupyter/ipykernel are optional interface packages. The method uses fixed arithmetic, not a trained machine-learning model; no random seed is required because no random sampling is performed.

src/prepare_inputs.py constructs the fixed scenarios and their rationales. src/career_methods.py implements validation, normalized skill sets, component scoring and ranking metrics. src/run_foundation.py validates and summarizes inputs. src/career_opportunity_recommender.ipynb presents the executed foundation followed by Week 2. results/week_1/ contains descriptive CSVs and an execution summary. src/protocol.json records the research question and scoring design.

## 5. Execute the foundation

From the repository root: (1) python -m pip install -r src/requirements.txt ; (2) python src/prepare_inputs.py ; (3) python src/run_foundation.py . Run these as separate commands. Alternatively open the notebook from the root or src folder and execute its Week 1 section in order. No external account, API key or network dataset is needed after dependency installation. Re-running input generation recreates the same fictional inputs; existing generated outputs are overwritten.

## 6. Current computational accomplishments

The executed foundation contains six complete profiles, twelve opportunities and 72 unique graded pairs. All nine checks passed, covering unique identifiers, unique and complete pair coverage, valid grades, required profile/opportunity fields, rationale presence and matching input digests. There are six distinct academic fields. profile_summary.csv, opportunity_summary.csv and grade_distribution.csv describe representative inputs. The foundation execution summary explicitly records that no comparative experiment is run by this stage.

## 7. Problems and design qualifications

No historical clicks, applications, placement outcomes or independently annotated relevance pairs are available. Hand-authored examples demonstrate technical feasibility but may favor the assumptions used in their design. Canonical skill names avoid synonym ambiguity rather than solving it. All listed preferences are soft ranking attributes; the model does not establish legal eligibility or minimum professional qualifications. The focused question is a measurable operationalization of the proposal, not evidence that broad career recommendation has been solved.

## 8. Planned work for the next milestone

The next implementation stage compares skill coverage alone with a fixed 0.60/0.25/0.15 score for skills, academic field and preferences. It adds known-example metric tests, executes the comparison and records improvements and failures without changing labels to favor the result. These reports organize Week 1 and Week 2 by milestone scope; both were prepared during the current work session and are not claims of earlier completion dates.
