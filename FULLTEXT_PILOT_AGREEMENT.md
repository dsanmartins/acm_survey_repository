# Historical full-text pilot agreement

The preserved initial 12-record aggregate matrix compares automated assessments (rows) with researcher assessments (columns):

| Automated / researcher | INCLUDE | EXCLUDE | UNCERTAIN |
|---|---:|---:|---:|
| INCLUDE | 9 | 0 | 0 |
| EXCLUDE | 0 | 1 | 0 |
| UNCERTAIN | 0 | 1 | 1 |

Observed agreement is 11/12 and chance-expected agreement is 85/144. Cohen's unweighted κ is exactly **47/59**, approximately 0.796610. Run `make verify-kappa` to recompute it from `data/methodology/fulltext_pilot_contingency.csv`. The original verifier and matrix are unchanged.

This is historical researcher–automated pilot agreement, not two-human-reviewer agreement or corpus-wide screening reliability. The reconciled nine-INCLUDE/three-EXCLUDE outcome does not supply the initial labels and is not used in the calculation. The package publishes only aggregate evidence; it does not establish recovery of unavailable original individual human annotations. The separate 40-record review and its seven reconciliations are explained in `METHODOLOGY.md`.
