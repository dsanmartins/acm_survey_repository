# Data dictionary and counting units

| File | Meaning and keys |
|---|---|
| `selected_publications.csv`, `bibliography/publications.csv` | Identical sanitized 243-record bibliographic index. `paper_id` is a publication record, not an assertion of independent study identity. Flags describe the historical bibliographic cohorts. |
| `bibliography/metadata_status.csv` | Existing identity/container verification statuses from the approved bibliography. LC0161's DOI/identity is confirmed, but its container title and year remain recorded local metadata rather than independently established by its chapter PDF. |
| `evidence_groups.csv` | 242 representative groups, explicit bibliographic manifestations, analytical/item-bearing flags and no independence assertion. |
| `bibliographic_to_evidence.csv` | One row per selected record, representative ID, DOI and manifestation role. Both MorphQ++ DOI remain. |
| `items.csv` | 1,554 counted extracted units: exact item ID, representative paper, RQ, evidence locator and original source-row SHA-256. |
| `item_correspondence.csv` | Historical original item IDs to counted representative IDs. Four alternative-manifestation items are aliases, not additional counted observations. |
| `scope_correspondence.csv` | Alternative/representative scope states and approved sets for the consolidated pair, preserving their differences without transferring assignments. |
| `scopes.csv` | 5,492 item–axis opportunities. `scope_id = item_id::axis`; state, approved set, authority and completion basis remain those of the selected canonical rows. |
| `memberships.csv` | 3,700 approved positive assignments to exact category/version, joined by scope and item. Multiple memberships are permitted where supported. |
| `taxonomies/categories.csv` | Unchanged 86-category registry, with historical IDs, versions and definitions. |
| `taxonomies/operational_definitions_22.csv` | Approved explanatory text: category name, definition, inclusion and exclusion/limits, with the existing ID for joining. No category or membership is added. |
| `rq5_pairing_proposals.csv` | 58 undecided, unapplied proposals. Stored references or co-occurrence are not approved links. |
| `rq2_family_level_not_mapped.csv` | 15 families × three test levels. All 45 entries remain blank and NOT_MAPPED, not numerical zero. |
| `selection/candidates_343.csv` | Original/final title–abstract and historical/effective full-text decisions, eligibility codes and terminal selection stage. Missing nonselected metadata remain blank. |
| `publication_page_ranges.csv` | Sanitized recorded inclusive page ranges; blank means no usable recorded span. |
| `methodology/fulltext_pilot_contingency.csv` | Aggregate initial automated rows versus researcher columns for 12 historical records. No individual reviewer annotations. |
| `provenance/reference_totals.json` | Current approved bibliographic/group totals, per-RQ denominators and pending-state contracts. |

`APPROVED_POSITIVE` has the exact registered set of positive memberships. `APPROVED_SCOPED_NONPOSITIVE` is a resolved absence of category fit within the assessed axis. `INCOMPLETE` and `CONTEXT_PROPOSAL_UNAPPLIED` remain unresolved; blank approved-set fields do not imply a negative finding. NR, NA and unclear judgments retain distinct meanings in the category definitions.

Coverage/category-support CSVs use evidence groups, items and scopes, with explicit denominators; their RQ populations overlap and must not be summed into a selection count. Figure 4 joins family and mode on the identical item. Bibliographic record counts in composition tables retain a denominator of 243. Observation of a quality problem, repository provenance and its classification are separate descriptors and may coexist when supported.
