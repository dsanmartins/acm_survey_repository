# Dataset guide

The source tables are **not independent study counts**. A publication can have multiple extracted items; each item can have several category-assessment scopes; an approved scope can have multiple category memberships.

| File | Row count | Primary key or join | Notes |
|---|---:|---|---|
| `data/selected_publications.csv` | 243 | `paper_id` | Title, authors, year, venue, DOI, document type, selection flags, RQ membership |
| `data/items.csv` | 1,558 | `item_id` | Join to publication through `paper_id` |
| `data/scopes.csv` | 5,506 | `scope_id` | Includes `scientific_state` and `approved_set_json`; incomplete is not negative |
| `data/memberships.csv` | 3,707 | (`scope_id`, `category_id`, `category_version`) | Only approved positive memberships |
| `data/taxonomies/categories.csv` | 86 | (`category_id`, `category_version`) | Versioned meaning of each category |
| `data/rq5_pairing_proposals.csv` | 58 | source-defined pairing identifier | All undecided; not approved operationalization links |

Bibliographic fields are carried from the approved selected-publication index; missing fields are preserved rather than fabricated. The classification values and evidence locators are not translated or recoded. A repeated `paper_id` across several RQ results is expected. The source inventory has 243 selected records, while downstream analytical coverage is 242, and 240 records have normalized items.

## Source-document composition (descriptive only)

`data/publication_page_ranges.csv` adds a `bibliographic_page_range` field to each of the 243 selected record IDs. A range `a-b` is measured inclusively as `b-a+1`; an empty field means no usable numeric range is available from the retained bibliographic metadata. `make composition` reproduces `results/composition/document_types.csv` and `results/composition/composition_summary.csv`. `publication_type` is the recorded document type, not an independently appraised primary/secondary study classification. No quality scores, family-merged study counts, or empirical maturity rankings are inferred.
