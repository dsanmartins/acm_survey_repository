# Publication-selection traceability (reviewer draft)

This repository now includes a **retrospectively assembled, record-level selection projection** built from original dated study-selection logs in a historical research artifact. It describes **343 unique candidate publication IDs**, with effective title-and-abstract decisions, full-text assessment states, and the **243 selected** records. It does not recreate missing subscription-database exports or establish 243 independent studies.

## Where to start

- [`data/selection/candidates_343.csv`](data/selection/candidates_343.csv): one row per unique candidate; original and final title/abstract decisions, effective full-text eligibility, exclusion code, and terminal stage. For selected publications the title, author, year and DOI (where available) come from the approved selected-publication index. For the remaining **100 candidates**, bibliographic metadata are absent from the compact selected-publication index and intentionally left blank.
- [`data/selection/stage_summary.csv`](data/selection/stage_summary.csv): audited stage counts (549 occurrences → 343 unique candidate IDs → 256 full-text inputs → 243 selected).
- [`data/selection/search_runs_8.csv`](data/selection/search_runs_8.csv): original per-database/per-query counts and hashes of the original source exports. Hashes document earlier exports, **not** included binaries or an independently reproducible search run.
- [`data/selection/primary_duplicate_occurrences_188.csv`](data/selection/primary_duplicate_occurrences_188.csv): matched, original primary duplicate occurrences, with their documented representative record IDs and matching rules.
- [`data/selection/supplementary_s4_occurrences_41.csv`](data/selection/supplementary_s4_occurrences_41.csv): supplementary S4 occurrences, duplicate relationships and addition status.
- [`selection_traceability.xlsx`](selection_traceability.xlsx): human-readable multisheet version, with identical derived accounting and caveats.

## Exact stage accounting

- Primary S1–S3: **508 occurrences**, **188 duplicate occurrences**, **320 unique primary candidates**.
- S4: **41 occurrences**, 15 S4 cross-database duplicates, 26 unique S4 records, of which three overlap primary candidates and **23 are new**.
- Total: **549 occurrences**, **206 duplicate/overlap occurrences**, **343 unique candidates**.
- Final title/abstract stage: **87 excluded**, **255 included**, **one uncertain case forwarded** = **256 full-text inputs**.
- Full-text effective decisions: **243 included**, **10 excluded**, **3 without scientific eligibility decisions** (two full texts not found; one bibliographic identity problem).
- Analytical denominators: 242 publications in the inventory and 240 with normalized RQ items, distinct from the 243 selected publications.

## Source lineage and limits

The frozen source is the prior project archive `QCC_CSUR_auditoria(1).zip`, specifically `docs/methodology/records/{search_inventory,title_abstract,title_abstract_original,search_runs,primary_duplicates,s4_occurrences}.csv` and `results/effective_screening/fulltext_effective_256.csv`. No researcher decision or search string was reconstructed from an inferred publication title. The ten effective full-text exclusions include one subsequent researcher-authorized E8 resolution. E8 documents a later **effective decision**, not an original E1–E7 rule retroactively inserted into the initial protocol. Three missing/identity cases have **no scientific exclusion** assigned.

A DOI, title or author for nonselected candidates should only be added after reconciling original source exports. Access to search-result exports is subject to Scopus/Web of Science terms and research authorization. A complete record-to-query bibliographic listing for all 549 occurrences is **not** delivered, and the 243 included records are not automatically independent studies. The Excel and CSV files are a provisional reviewer-facing **candidate release** until the researchers approve which historic metadata may be distributed; **no Zenodo DOI is claimed**.
