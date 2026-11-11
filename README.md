# Quantum Software Quality — Reproducibility repository

This **repository-only** package accompanies the separately distributed article and supplementary material, *Quantum Software Quality: Evidence, Assurance Mechanisms, and Model-Level Limits—A Systematic Survey*, prepared for peer review in ACM manuscript format. No LaTeX manuscript, compiled article/supplement PDF, or validated figure PDF is included in this repository. 

Start with [`REVIEWER_START_HERE.md`](REVIEWER_START_HERE.md) for a short, command-by-command reproduction guide.

## Quick start

With Python 3 installed, open a terminal at the root of this extracted repository:

```bash
make verify
make reproduce
```

- `make verify`: checks the 243/242/240 publication populations, classification results, reference CSVs, and repository file hashes.
- `make reproduce`: regenerates `coverage.csv`, `category_support.csv`, and `rq2_bubble.csv` under `results/reproduced/` from approved public data. It does not modify the approved classification inputs or run quantum simulations.
- `make composition`: recalculates descriptive source-document types and page-span availability from the 243-record bibliography. It does **not** classify research designs, grade studies, or merge related publications.
- The original author-supplied Scopus and Web of Science search texts for S1–S4 are now in [`search_strings/`](search_strings/). Read [`SEARCH_STRINGS.md`](SEARCH_STRINGS.md) before attempting any new database search. The historical 549 search occurrences cannot be regenerated from query text alone.
- To compile the article and supplement, extract the **manuscript ZIP** and run `bash build_acm.sh` inside its root; it contains the ACM 2.21 class and the original PDF figures.

## Repository directory map

| Location | Contents | How to use |
|---|---|---|
| `data/selected_publications.csv` and `.xlsx` | Catalogue of 243 selected publications: LC identifier, authors, title, year, venue, DOI, RQ membership and corpus flags | Find a source and its inclusion state |
| `data/bibliography/publications.csv` | Canonical 243-publication bibliography inventory | Cross-check publication metadata |
| `data/publication_page_ranges.csv` | Sanitized recorded page ranges for 243 publications | Reproduce the supplementary bibliography-composition table; missing page ranges are explicitly blank |
| `data/items.csv` | 1,558 extracted RQ items | Join `paper_id` from catalogue to `item_id` |
| `data/scopes.csv` | 5,506 classification scopes and approval states | Inspect evidence-backed positive/empty and incomplete states |
| `data/memberships.csv` | 3,707 approved positive category memberships | Join using `scope_id` |
| `data/taxonomies/categories.csv` | 86 versioned definitions | Interpret category identifiers |
| `data/rq5_pairing_proposals.csv` | 58 undecided proposed pairings | Confirm none is promoted to an approved link |
| `data/provenance/` | Frozen aggregate reference totals | Check the documented scientific inventory |
| `results/reference/` | Approved expected summary CSVs | Compare reproduced results |
| `results/reproduced/` | Output of `make reproduce` | Inspect recalculated summaries |
| `results/composition/` | Recalculated document-type and page-span summaries | Check Supplementary Table S10 without treating document types as study-quality ratings |
| `scripts/` | Reproduction and verification programs | Run read-only/integrity checks |
| `figure_sources/` | Available Python figure sources, including current reader-facing Figure 1 and illustrative Figure 4 | Inspect or edit scripts; figure generation is outside `make reproduce` and may require assets from the separate manuscript |
| `search_strings/` | Eight original Scopus/Web of Science text queries (S1–S4) | Review exact author-supplied query wording; database results and historical search logs are not included |
| `SEARCH_STRINGS.md` | Query-to-database mapping, dates, file hashes, rerun limitations | Follow the search strategy and provenance without treating a contemporary rerun as the historical set |
| `licenses/` | Included license notices | Inspect applicable terms |

## Link to the manuscript tables

In the current article, **Table 2** gives study eligibility criteria and rationales, and **Table 3** summarizes the scientific findings and limits of RQ1--RQ5. Detailed audit counts have been moved to **Supplementary Table S8**. These counts can be checked directly against `results/reference/coverage.csv` and reproduced with `make reproduce`. Supporting publication and item counts for the reported categories are in `results/reference/category_support.csv`. The 28 same-item technique-family/analysis-mode cells underlying Figure 3 can be checked in `results/reference/rq2_bubble.csv`.

The supplementary **Table S10** summarizes source-document types and available page spans using `make composition`. It does not estimate the number of independent studies or risk of bias. Candidate publication families, identified through metadata similarities, have not been scientifically adjudicated and are not consolidated into the corpus.

The repository uses classification states for traceability; those states should not be interpreted as scientific findings about the absence of defects or mechanisms. Classification inputs and researcher decisions have not been changed by the editorial restructuring.

## How to trace a publication and classification

1. Locate an identifier such as `LC0297` in `data/selected_publications.csv`.
2. Find related records by `paper_id` in `data/items.csv`.
3. Join `item_id` to `data/scopes.csv` and inspect axis-level decisions.
4. Join approved positive `scope_id` values to `data/memberships.csv`.
5. Decode `category_id` plus `category_version` via `data/taxonomies/categories.csv`.
6. Run `make reproduce` and compare `results/reproduced/` with `results/reference/`.

A publication can contain multiple items and an item can have several assessment scopes. Category memberships are not independent-study counts. The 243 selected records include 242 in the analytical inventory and 240 with normalized RQ items. This repository reproduces curated analyses, **not** full-text screening or extraction from copyrighted sources.

## Query texts and current manuscript figure sources

The author-supplied S1–S4 query strings for Scopus and Web of Science are included under `search_strings/` (see `SEARCH_STRINGS.md` for source-archive provenance). The current manuscript introduces a compact, illustrative seven-field diagram as Figure 4; its editable source is `figure_sources/assurance_reporting_schema.py`. The cleaned selection flow of Figure 1 uses `figure_sources/study_selection_clean.py`, which requires the authoritative source diagram **from the separate manuscript ZIP**. The companion manuscript still contains all original validated figures; this data repository does not redistribute their PDFs.

## Scope and permissions

The separate manuscript archive includes 11 original, scientifically validated PDF figures and the approved researcher-process declaration. This repository archive includes Python figure source where available, but it does not claim standalone regeneration of all 11 PDFs. There is no Qiskit execution requirement. The overall review package remains a private reviewer-draft candidate subject to final release and rights checks. See `RIGHTS_AND_LIMITATIONS.md` and `REPRODUCIBILITY.md`.
