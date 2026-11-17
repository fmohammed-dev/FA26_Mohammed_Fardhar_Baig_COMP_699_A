# Extension 1 labeling protocol (pre-evaluation)

The six profiles S07-S12 are fictional. The original 12 opportunity records O01-O12 are used unchanged. There are 72 provisional profile-opportunity annotations. No real student or job data is included.

## Separate concepts
- **Relevance grade (0-2):** 0 = no useful role/domain fit; 1 = partial or transferable fit with important gaps; 2 = strong skill/domain fit. Preference conflicts can be explained in the rationale but do not automatically force grade 0. This is a research annotation, not a recommendation result.
- **Preference compatibility:** Two explicit Boolean observations: desired employment type matches the opportunity type, and opportunity work mode belongs to the preferred modes. A mismatch is a soft preference conflict, not evidence of legal or employer ineligibility.
- **Hard eligibility:** `eligibility_status=not_assessed` for all pairs. Original opportunity records do not contain verified eligibility criteria (such as work authorization, credentials, or location restrictions). No hard-eligibility filtering is justified until separately documented criteria are added. Do not equate `accepted_fields` with mandatory eligibility.

## Review process
All labels are `author_provisional`. Independent relevance and eligibility review is **not completed**. A reviewer should examine blinded scenario descriptions and rationales without seeing model scores, document disagreements, and freeze adjudicated labels before running evaluation. Never describe these provisional grades as independent ground truth.

## Split and leakage control
Development: S07-S09; held-out evaluation: S10-S12. The opportunity catalog is shared; this is a **profile-level**, not opportunity-level, holdout. Do not inspect evaluation metrics to tune weights or rules. No scoring or performance results have been generated for this extension.
