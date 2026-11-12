# Zenodo deposit — existing DOI and revised-archive checklist

**Existing deposit DOI (author supplied):** https://doi.org/10.5281/zenodo.24168011

**Status of this local ZIP:** a subsequent documentation-only revision aligned with the paper title *Quantum Software Quality: Evidence, Assurance Mechanisms, and Model-Level Limits—A Survey*. The DOI refers to an existing deposit, **not automatically to the revised ZIP**. Neither its current Zenodo license metadata nor its file identity is independently verified by this package.

## Before creating a new Zenodo version

1. Confirm the exact version and contents currently associated with the DOI; retain the existing deposit as an immutable historical record.
2. Obtain coauthor agreement for the changes in title/description and the revised archive; confirm ownership and applicable permissions for source, documentation, derived data and figure files.
3. Inspect the metadata, rights and redistribution conditions for candidate-level bibliographic and selection information. No licensed Scopus or Web of Science raw exports or reviewed papers should be added without authorization.
4. Confirm that `selection_traceability.xlsx` contains no private reviewer comments, third-party full texts, account identifiers or other confidential information. The current workbook omits bibliographic title/DOI/author metadata for the 100 nonselected candidates; do not infer it.
5. Run `make verify`, `make reproduce`, `make composition` and `make figures-conceptual` on a clean extraction. Confirm the published ZIP's SHA256 and file list.
6. Reconcile the Zenodo license field with the MIT and CC-BY-4.0 notices under `licenses/`; determine their scope before releasing any revised version. Do not silently relicense collaboratively authored materials.
7. Update the Zenodo title and description to match the finalized *A Survey* framing; link the corresponding manuscript, and create a **new version** if the ZIP's bytes are to be updated.
8. After publishing, record the version-specific DOI, release date, Zenodo version number and SHA256 in this document or the release notes, then update the manuscript if a new persistent identifier is required.

## Release record

- Existing DOI, supplied by the authors: https://doi.org/10.5281/zenodo.24168011
- Publication date and Zenodo license metadata: **not verified here**.
- New version corresponding exactly to this revised ZIP: **not yet published or independently confirmed**.
- Scientific results and figure content: **unchanged by this editorial update**.
