# Historical full-text pilot agreement (aggregate evidence)

The frozen full-text pilot had **12 publication records** independently assessed
by a **researcher** and an **automated screening procedure** with labels
`INCLUDE`, `EXCLUDE`, and `UNCERTAIN`, prior to reconciliation.
The preserved historical aggregate matrix is in
[`data/methodology/fulltext_pilot_contingency.csv`](data/methodology/fulltext_pilot_contingency.csv).
Its **rows** are initial automated decisions and its **columns** are initial
researcher decisions; this orientation follows the original internal record
`docs/methodology/records/historical_accounting.json` (supplied by the authors).

| Initial automated / researcher | INCLUDE | EXCLUDE | UNCERTAIN |
|---|---:|---:|---:|
| INCLUDE | 9 | 0 | 0 |
| EXCLUDE | 0 | 1 | 0 |
| UNCERTAIN | 0 | 1 | 1 |

The observed agreement is `11/12`, chance-expected agreement is `85/144`
from the two marginal distributions, and unweighted Cohen's kappa is
`(11/12 - 85/144)/(1 - 85/144) = 47/59 = 0.796610169...`.

Reproduce with:

```sh
python3 scripts/verify_kappa.py
```

The historical *reconciled* outcome was nine INCLUDE and three EXCLUDE;
these reconciled labels are not used to calculate agreement. This is a
small, purposively selected pilot and is **not** a whole-corpus reliability
estimate or inter-rater agreement between two human researchers.

**Provenance and release boundary.** The aggregate values and validation
algorithm were recovered from the supplied historical
`historical_accounting.json`, `methodology.py`, `STUDY_SELECTION.md`, and
`VALIDATION_REPORT.md` (and corroborated by `QCC-FT-1.1.md`). To avoid
publishing unrelated historical/private files and an internal script with
non-public dependencies, this archive includes only the aggregate matrix,
a new standalone reproducer, and this explanation. No paper-level reviewer
decisions, private full texts, search exports, or individual identities are
included. These aggregate values must remain distinguished from decisions
in the reconciled screening trace.
