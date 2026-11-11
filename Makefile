.PHONY: verify reproduce composition help
help:
	@printf '%s\n' 'make verify       Check publication totals, scientific outputs, and integrity hashes' 'make reproduce    Regenerate the three analysis CSVs' 'make composition  Reproduce source-document type and page-span summaries'
verify:
	python3 scripts/analyze_corpus_composition.py --check
	python3 scripts/reproduce_analysis.py --check
	python3 scripts/verify_repository.py
reproduce:
	python3 scripts/reproduce_analysis.py

composition:
	python3 scripts/analyze_corpus_composition.py
