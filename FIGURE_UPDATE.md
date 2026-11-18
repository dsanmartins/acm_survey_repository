# Current main and supplementary figure correspondence

The approved article has **six main figures**:

| Figure | Content | Reproduction available here |
|---|---|---|
| 1 | Bibliographic selection and subsequent analytical coverage | Public selection counts are verified. Native source-PDF chain needs the separate approved manuscript assets; the 243 selected records remain unchanged. |
| 2 | Five complementary taxonomy dimensions | Registry contains all 86 categories. Full native rendering needs the approved manuscript environment. |
| 3 | Conceptual organization of RQ1 quality phenomena | Approved PDF/PNG bundled; unchanged current source regenerates with `make figures-conceptual`. |
| 4 | RQ2 same-item technique-family/analysis-mode evidence map | `make reproduce` regenerates the exact 28 cells and 381 associated items; the approved current PNG and renderer source are supplied. Native publication rendering needs manuscript dependencies. |
| 5 | Illustrative seven-field assurance-claim reporting schema | Unchanged approved source regenerates with `make figures-public` (Matplotlib). Its example describes a procedure, not a newly observed verdict. |
| 6 | RQ3–RQ5 representation, condition and model-level implications | Approved PDF/PNG bundled; generated with the Figure 3 source. This map was previously referred to as Figure 7; that numbering is obsolete for the current article. |

The supplemental test-level panel uses the consolidated inventory of 449 RQ2 items and 181 evidence groups; positive item marginals are 16/8/6 for Unit/Integration/System, with 21 groups in their union. These marginals establish no family–level joint mapping. Complete taxonomy panels and the ideal-state illustration remain supplemental, not additional main figures. No figure is added as a seventh main figure.

All original nine Python scripts remain byte-identical for provenance. Approved current copies are supplied with `current_` filenames where the source evolved. Historical sources may require the source-layout modules and frozen inputs of their original manuscript environment; they are not advertised as standalone consolidated reproducers. Use the supported Make targets and see `figure_sources/README.md`.

The eleven original scientific PDF assets remain in the separate manuscript source package under the existing distribution policy. Their approved hashes and the current compiled manuscript/supplement hashes are recorded in `data/provenance/manuscript_assets.json`. The two bundled concept-map PDFs are author-generated explanatory illustrations, not third-party papers or those eleven original assets.

Numerical identity, figure regeneration, LaTeX compilation and binary PDF identity are separate claims. This repository ZIP does not include a manuscript compilation target, nor does a successful conceptual render resolve the historical native SIGSEGV cause.
