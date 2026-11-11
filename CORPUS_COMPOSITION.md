# Interpreting bibliographic composition

The 243 selected publication IDs are *publication records*, not verified independent studies. Source-document types are retained from the bibliographic metadata and may not be reliable indicators of whether a source is primary or secondary research. Page-span metadata (when present) are descriptive, and a short span is not a quality grade. No related publications were merged or relabeled as independent replications.

Run `make composition` to reproduce Supplementary Table S10 and inspect `results/composition/`. The individual source fields are in `data/selected_publications.csv` and `data/publication_page_ranges.csv`. Missing page spans are blank rather than zero. This analysis did not redo full-text screening, primary-study appraisal, or publication-family consolidation. All existing RQ classifications were preserved.
