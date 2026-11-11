# Scientific reproduction guide (repository-only archive)

This archive reproduces selected aggregate analyses based on curated and approved public projection data. Read `README.md` first for the data map, units of analysis, and joins.

## Reproduce the reported summary tables

```bash
make verify
make reproduce
```

`make reproduce` regenerates the following under `results/reproduced/`:

- `coverage.csv`: five RQ rows with item counts, axis-specific scopes, positive and bounded-empty sets, memberships and pending scopes.
- `category_support.csv`: supporting items and distinct publications for each versioned classification category.
- `rq2_bubble.csv`: 28 observed same-item technique-family × analysis-mode combinations and supporting publications.

Outputs are checked byte-for-byte against `results/reference/`; any discrepancy causes a nonzero exit code. The 58 proposed RQ5 pairing links remain undecided. No data are imputed.

## Follow a published reference

`data/selected_publications.csv` lists 243 selected publication records and their `LC` identifiers. Join `paper_id` to `data/items.csv`, `item_id` to `data/scopes.csv`, approved `scope_id` to `data/memberships.csv`, and versioned category keys to `data/taxonomies/categories.csv`. See `DATA_DICTIONARY.md`.

## Article and figure assets

The separately distributed separate **manuscript ZIP** contains the article and supplement LaTeX sources, ACM 2.21 files, both compiled PDFs, 11 unchanged scientific PDF figures, and the relevant source-item locator tables in the supplement. Compile it by running `bash build_acm.sh` inside its extracted root. This repository-only archive does not include those assets. `figure_sources/` contains available Python source files but the compact reproduction workflow does not overwrite validated PDF figures; full independent rendering of every figure is not promised.

## Database search text (not an automatic re-execution)

The `search_strings/` directory now contains the eight verbatim S1–S4 queries for Scopus and Web of Science; see `SEARCH_STRINGS.md` for the database mappings and query file checksums. They can be inspected or rerun manually with database access, but index updates and current filters may produce different results. Historical result exports and individual record-to-query provenance are not included; the 549 original search occurrences cannot be independently reconstituted from these files alone.

## Boundaries

This workflow does not rerun original full-text screening, independently assess the source studies, reproduce the full private research workspace, or execute Qiskit. Historical validation statuses remain distinct from the tests reproduced here. Redistribution remains subject to the documented rights review.
