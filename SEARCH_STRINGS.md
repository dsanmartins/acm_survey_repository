# Search strings and search-strategy reproducibility

This directory contains the **eight original text files supplied by the authors** in `search_strings.zip` for the systematic search protocol, reproduced byte-for-byte. They were not in the previous curated reviewer repository.

## Mapping to databases and search groups

| Search group | Scopus query | Web of Science query | Scope |
|---|---|---|---|
| S1 | [`scopus_s1.txt`](search_strings/scopus_s1.txt) | [`wos_s1.txt`](search_strings/wos_s1.txt) | Quantum software faults, bugs, defects, static analysis, testing, mutation testing, and validation |
| S2 | [`scopus_s2.txt`](search_strings/scopus_s2.txt) | [`wos_s2.txt`](search_strings/wos_s2.txt) | Model-driven engineering, metamodels, DSLs, UML, software representations |
| S3 | [`scopus_s3.txt`](search_strings/scopus_s3.txt) | [`wos_s3.txt`](search_strings/wos_s3.txt) | Constraints, invariants, well-formedness, model and structural validation |
| S4 | [`scopus_s4.txt`](search_strings/scopus_s4.txt) | [`wos_s4.txt`](search_strings/wos_s4.txt) | Supplementary terminology: bug fixes, code smells, variability, modeling strategies, structural/configuration constraints |

The manuscript reports searches on **30 September 2026** (S1–S3) and supplementary searches on **1 October 2026** (S4). Those dates describe the documented research protocol; ZIP file timestamps are **not** independent execution records. The uploaded text uses the database-specific syntax `TITLE-ABS-KEY(...)` in Scopus and `TS=(...)` in Web of Science. Exact query spelling, wildcards, parentheses and line breaks have **not** been normalized, repaired, or rewritten.

## How to inspect or rerun

1. Open the relevant `.txt` file in `search_strings/`.
2. Copy its exact contents into the corresponding database advanced search interface, subject to current database syntax and access restrictions.
3. If independently rerunning, record the execution date, database version/coverage, filters applied, and retrieved counts. Treat the resulting hit set as a **new run**, not necessarily as the historical 2026 hit set.

No licensed Scopus/Web of Science exports, original result snapshots, or individual record-to-query mappings are distributed. Thus, the presence of query strings **improves transparency** but does not independently reproduce the historical **549 retrieved occurrences**, deduplication, full-text selection, or review decisions. `make verify`, `make reproduce`, and `make composition` still validate only curated research data, not live database queries. The supplied text files establish the query text submitted for this package, not independent proof of their historical execution. The repository's private reviewer-draft release status remains unchanged.

## Provenance and integrity

- Source attachment: `search_strings.zip` supplied by the user on 11 November 2026.
- Source attachment SHA256: `68e1b90d772610d62bdacd0e57e6320e560e63e16c8c3bd5e908ef47d15039da`.
- SHA256 hashes and byte lengths of each individual text file: [`search_strings/SEARCH_STRING_HASHES.csv`](search_strings/SEARCH_STRING_HASHES.csv).
- Repository-wide SHA256 verification: `MANIFEST_SHA256.csv` and `make verify`.
