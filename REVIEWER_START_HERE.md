# Reviewer quick start — quantum software quality survey

This companion data archive is **separate from** the LaTeX manuscript archive. It contains curated, sanitized data, deterministic analyses, and the **eight author-supplied database search strings (S1–S4)**. It does **not** reproduce the historical database results, eligibility judgments, or extraction from copyrighted full texts.

## Read the study

Read `build/main.pdf` and `build/supplement.pdf` in the **separate manuscript ZIP**. The main article presents the five RQ findings and their evidential boundaries. The supplement includes the classification audit table (Table S8), representation/obligation examples (Table S9), and source-document composition (Table S10).

## Reproduce the quantitative outputs

Requirements: Python 3 and GNU Make (or run the Python scripts directly). No quantum simulator or Qiskit installation is needed for the documented analytical checks.

From the root of **this extracted repository** run:

```bash
make verify
make reproduce
make composition
```

- `make verify` confirms curated publication populations and repository integrity, and checks the three expected scientific outputs.
- `make reproduce` regenerates the five-row RQ coverage table, the category-support data, and the 28 observed RQ2 family/mode combinations under `results/reproduced/`. They are compared with `results/reference/`.
- `make composition` reproduces the bibliographic composition summary for Supplementary Table S10.

**Do not interpret a successful run as a repetition of the source searches or independent validation of each extracted statement.** Unresolved classifications and proposed relationships retain their documented status.

## Inspect the original search strings

The author-supplied search texts are in `search_strings/scopus_s1.txt` through `scopus_s4.txt` and `search_strings/wos_s1.txt` through `wos_s4.txt`. See `SEARCH_STRINGS.md` for exact mappings, the supplied archive checksum, and limits of contemporary reruns. The licensed search-result exports and historical database snapshots are **not** distributed. Query files are not executed by `make verify` or `make reproduce`.

## Trace a publication to a category

1. Find `LCxxxx` in `data/selected_publications.csv` (or `.xlsx`), including title, authors, year, venue, DOI (when available) and RQ membership.
2. Join `paper_id` to `data/items.csv`; then join `item_id` to `data/scopes.csv`.
3. For an approved positive scope, join `scope_id` to `data/memberships.csv`.
4. Interpret the category using `data/taxonomies/categories.csv` and its registered version.
5. Consult the publication/source-evidence locators in the separate supplementary PDF to interpret the conclusion in context.

## Where to find the main cross-checks

| Scientific claim | Repository data |
|---|---|
| 243 selected / 242 analytical / 240 with normalized RQ items | `data/selected_publications.csv` |
| RQ1–RQ5 classification accounting (Supplementary Table S8) | `results/reference/coverage.csv` |
| Category support (Supplementary Tables S1–S5) | `results/reference/category_support.csv` |
| RQ2 joint evidence map (Figure 3) | `results/reference/rq2_bubble.csv` |
| Publication types and page spans (Supplementary Table S10) | `results/composition/` |
| 58 undecided RQ5 pairing proposals | `data/rq5_pairing_proposals.csv` |

## Limits and access

No source-study full texts, licensed database exports, or private reviewer evidence are included. The 11 original PDF figures and manuscript LaTeX sources belong to the **separate manuscript ZIP** and have not been redrawn. Some figure-source scripts require components outside the compact reproduction workflow and are supplied only for inspection. The data package is a private reviewer candidate; public release and a persistent DOI remain separate approval steps. See `RIGHTS_AND_LIMITATIONS.md`.
