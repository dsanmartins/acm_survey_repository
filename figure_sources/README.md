# Editable scientific figure source files

This directory contains the available original scientific figure Python sources plus two scripts used by the latest manuscript's **editorial figures**:

- `study_selection_clean.py` produces the reader-facing **Figure 1** by replacing operational wording in the preserved `figures/study_selection.pdf` design. It requires PyMuPDF, a copy of the **original PDF in the separate manuscript ZIP**, and suitable font files in the local rendering environment. This repository intentionally does **not** include or change the scientific PDF.
- `assurance_reporting_schema.py` generates the current **Figure 4**, an **illustrative** seven-field assurance-reporting diagram with a QASMInfer example. It requires Matplotlib, produces a PDF and PNG under a local `figures/` folder when explicitly run, and does not compute scientific outcomes. Possible statistical verdicts in that illustration are not newly observed results.

Other Python scripts here are retained from the original scientific workflow for provenance and controlled editing. Some require external modules or historical analysis assets unavailable in this compact repository. The approved original scientific PDFs are in the **separate manuscript ZIP**; figure scripts are not invoked by `make verify` or `make reproduce`, and this package does not promise that every figure can be regenerated in isolation. Qiskit is deliberately **not** executed as part of the review workflow.
