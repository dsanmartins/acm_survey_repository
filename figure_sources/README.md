# Figure sources and executable scope

Main-figure correspondence is specified in `../FIGURE_UPDATE.md`; the RQ3–RQ5 map is Figure 6. There are six main figures.

Supported public commands:

```sh
make figures-conceptual   # Figures 3 and 6
make figures-public      # Figures 3, 5 and 6
```

Dependencies: Python 3 and Matplotlib (including its normal NumPy/Pillow/font dependencies). The approved sources use DejaVu Sans and fixed drawing parameters; no quantum simulator, private records or network is needed. Generated outputs go to `results/generated_figures/`, preserving packaged reference assets.

The conceptual source is `current_conceptual_maps.py`; the Figure 5 source is `assurance_reporting_schema.py`. Both are unchanged copies of approved manuscript sources. The wrapper isolates their normal output locations rather than editing the drawing code. Colors, dimensions and labels remain editable in those Python files for future authorized work.

The nine original scripts are retained exactly: `conceptual_maps.py`, `assurance_reporting_schema.py`, `circuit_illustration.py`, `fig01_public.py`, `fig01_study_selection.py`, `fig02_taxonomy_tree.py`, `fig03_rq2_bubble.py`, `rq2_test_levels.py`, and `study_selection_clean.py`. The originals are provenance, not a claim that historical data contracts now describe the consolidated results.

Approved current Figure 1, taxonomy, Figure 4 and test-level sources are also supplied with `current_` prefixes. Native execution requires the matching manuscript source layout and dependencies: local `qcc` data/plotting modules; Matplotlib; FontTools for native typography; TeX font discovery (`kpsewhich`) where used; and PyMuPDF for the original selection-PDF chain. Read the source imports and the approved manuscript environment's requirements. These are deliberately not dependencies of the four standard-library numerical Make targets.

Figure 4's exact 28-cell/381-item numerical reproduction is provided by `scripts/reproduce_analysis.py`, independently of native rendering. The eleven original scientific PDFs remain in the separate manuscript source package. Do not run a historical raw-publication renderer against the consolidated CSVs or interpret undocumented missing dependencies as a passed regeneration test.
