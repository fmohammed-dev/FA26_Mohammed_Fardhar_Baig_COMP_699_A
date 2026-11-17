# Extension 1: graduate career matching scenarios

This research-only extension adds 6 fictional profiles (S07-S12) against the **unchanged** 12 original opportunities, for 72 provisional profile-opportunity annotations. The original `data/synthetic/` benchmark and its frozen manifest are not modified.

- `profiles.json`: six scenarios with conflicting work-mode/type preferences and transferable academic backgrounds.
- `labels.json`: author-provisional relevance grades, separately observed type/mode compatibility, and **not-assessed** hard eligibility.
- `labeling_rubric.md`: definitions and independent-review procedure.
- `split.json`: fixed development profiles S07-S09 and evaluation profiles S10-S12.
- `manifest.json`: SHA-256 hashes of the extension artifacts.

The shared 12-opportunity candidate catalog is `data/synthetic/opportunities.json`. This extension has **not** been scored. The evaluation set must not be used for tuning.
