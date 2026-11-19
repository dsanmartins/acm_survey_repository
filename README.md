# Quantum Software Quality: Evidence, Assurance Mechanisms, and Model-Level Limits—A Survey

This is the updated existing reproduction package for the approved survey. It retains the original repository structure and scientific identifiers. Version **2.0.0** was published on **2026-11-18** in the [GitHub release](https://github.com/dsanmartins/acm_survey_repository/releases/tag/v2.0.0) and [Zenodo version record](https://doi.org/10.5281/zenodo.24349998). This post-publication documentary correction describes the final approved manuscript; it does not replace or retrospectively update the archived v2.0.0 files.

## Start here

From the extracted `acm_survey_repository/` directory, with Python 3 and Make:

```sh
make verify
make verify-kappa
make reproduce
make composition
```

These four commands require only the Python standard library. They use files inside this package, without the development repository, private records, database subscriptions or network access. `make verify` checks the complete file manifest, record identities, classification relations and byte-for-byte numerical reproduction. The archived `MANIFEST_SHA256.csv` retains the published v2.0.0 hashes. In this working copy, the six approved documentary corrections differ from that manifest, so the complete manifest check will report a documentary mismatch. The manifest and validators have not been changed; this does not indicate a change to scientific inputs or results.

## Counting units

| Unit | Count |
|---|---:|
| Selected bibliographic records | 243 |
| Selected consolidated evidence groups | 242 |
| Groups with analytical records | 241 |
| Groups with normalized items | 239 |
| Extracted items / classification scopes / positive memberships | 1,554 / 5,492 / 3,700 |
| Existing categories | 86 |
| Figure 4 same-item family–mode cells / associated items | 28 / 381 |
| Undecided RQ5 pairings / unmapped family–level cells | 58 / 45 |

LC0173 and LC0174 are bibliographic manifestations of the same documented MorphQ++ study. Both remain selected, with both DOI. LC0173 represents their scientific evidence; LC0174 is an alternative manifestation. This is not an eligibility exclusion and does not establish independence of the other groups. The historical bibliographic flags still describe **243/242/240 publication records**; the consolidated scientific denominators are **242/241/239 groups**.

## Files and scientific traceability

- `data/selected_publications.csv` and `data/bibliography/publications.csv`: the same sanitized 243-record catalogue; XLSX is a view of those public cells.
- `data/bibliography/metadata_status.csv`: source-specific identity/container verification status. Recorded local metadata are not automatically independently confirmed bibliographic facts; LC0161 retains a container-title limitation.
- `data/selection/` and `selection_traceability.xlsx`: recorded selection decisions for 343 candidates, with metadata for selected records only. No missing identities are invented.
- `data/evidence_groups.csv`, `bibliographic_to_evidence.csv`, `item_correspondence.csv` and `scope_correspondence.csv`: explicit manifestation/group and item correspondence, retaining historical IDs and the original classification differences without transferring memberships.
- `data/items.csv`, `scopes.csv` and `memberships.csv`: the approved consolidated view. A `paper_id` identifies its representative publication; joins are through exact item/scope/category/version identifiers.
- `data/taxonomies/categories.csv`: the unchanged 86-category registry. The 22 approved explanatory definitions are in `operational_definitions_22.csv` and `docs/operational_category_definitions.tex`; they create no category or reclassification.
- `results/reference/` and `results/reproduced/`: coverage, category support, same-item Figure 4 cells and per-axis coverage. The files reproduce the approved numerical sources exactly.

Read [DATA_DICTIONARY.md](DATA_DICTIONARY.md), [METHODOLOGY.md](METHODOLOGY.md) and [docs/CATEGORY_DEFINITIONS.md](docs/CATEGORY_DEFINITIONS.md). Blank, incomplete, scoped nonpositive and unreported states have different meanings; none should be converted into an unobserved scientific result.

## Tables and figures

Coverage and category support underpin the main and supplemental result tables, including S1, S2, S4 and S8. Figure 4 is reconstructed numerically in `results/reproduced/rq2_bubble.csv`, including all 28 cells and their exact 381 item identities. Family–level associations remain unmapped; their 45 blank cells are not observed zeroes.

The final approved article has **seven** main figures. **Figure 6** shows the three ideal circuits A–B–C; the representation–condition–model-level comparison is **Figure 7**. Supplementary Figure S2 and its derivations remain in the supplement. See [FIGURE_UPDATE.md](FIGURE_UPDATE.md) for the complete mapping and generation scope. Optional `make figures-public` regenerates the author-created Figures 3, 5 and 7 using Matplotlib. This target does not regenerate the final article's circuit Figure 6. The original nine figure scripts are preserved; approved newer versions are supplied separately, with their dependencies declared. Their historical filenames do not determine current numbering.

The eleven original scientific PDF figures remain in the separately supplied manuscript sources, not this repository ZIP. This package does not claim standalone compilation of the manuscript or regeneration of all original PDFs. Numerical reproduction, figure generation, LaTeX compilation and PDF binary identity are separate checks.

## Version and rights

Upstream: https://github.com/dsanmartins/acm_survey_repository . The published package was prepared from the existing content based on commit `f3093ca18de13d8b175e3b60a056dfd392cf6832`; it contains no `.git` directory. The original Git history is preserved outside the distribution.

The version-specific DOI for **2.0.0** is **10.5281/zenodo.24349998**. The concept DOI **10.5281/zenodo.24168010** identifies the version lineage; **10.5281/zenodo.24168011** identifies historical version **1.0**. These identifiers describe the published records, not a new deposit of this documentary correction. The historical license notices are preserved. The new scoped CC BY 4.0 grant and retained MIT/component terms are explained below. See [RIGHTS_AND_LIMITATIONS.md](RIGHTS_AND_LIMITATIONS.md) and [ZENODO_RELEASE_CHECKLIST.md](ZENODO_RELEASE_CHECKLIST.md). Earlier release notes describe their historical versions, not the current consolidated counts.

## License

Original QCC data curation, results, category definitions, documentation and original figure designs covered by `LICENSE_MATRIX.csv` are licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) (CC-BY-4.0); the full official legal code is in [LICENSE](LICENSE). Credit Daniel San Martín, Paul Leger, and Valter Vieira de Camargo using [CITATION.cff](CITATION.cff), retain applicable notices and the license link, and indicate changes. Do not imply endorsement.

Original code and build configuration retain [MIT](licenses/MIT.txt). Embedded font components retain their own notices. See [LICENSE_SCOPE.md](LICENSE_SCOPE.md), [LICENSE_MATRIX.csv](LICENSE_MATRIX.csv) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for exact exceptions. Cited publications and externally owned metadata are not relicensed. The six complete bibliographic files are preserved, including both spreadsheets. Authorized institutional research access is confirmed by the authors; the applicable redistribution clause and retrieval route remain unverified. No prohibition or special copyright permission for ordinary bibliographic facts is inferred. Their RIGHTS_REVIEW_REQUIRED entries are a documentary reservation, not a finding of unlawful content. Publication of v2.0.0 does not establish resolution of that documentary reservation; see RIGHTS_AND_LIMITATIONS.md.

The `v2.0.0` publication status and preserved preparation notes are in [CHANGELOG.md](CHANGELOG.md). `.zenodo.json` supplies scoped-license and historical-lineage information for review; it does not create a record or DOI. If both citation files are present, Zenodo's GitHub integration uses `.zenodo.json` rather than `CITATION.cff`.
