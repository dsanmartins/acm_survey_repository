PYTHON ?= python3
export PYTHONDONTWRITEBYTECODE := 1
.PHONY: verify verify-kappa reproduce composition figures-conceptual figures-public help
help:
	@printf '%s\n' 'make verify          Verify hashes, scientific identities and numerical references' 'make verify-kappa    Reproduce the historical researcher–automated pilot' 'make reproduce       Reproduce four consolidated analysis CSVs' 'make composition     Describe bibliographic records and evidence-group denominators' 'make figures-public  Regenerate Figures 3, 5 and 6 (Matplotlib required)'
verify:
	$(PYTHON) -B scripts/reproduce_analysis.py --check
	$(PYTHON) -B scripts/analyze_corpus_composition.py --check
	$(PYTHON) -B scripts/verify_kappa.py
	$(PYTHON) -B scripts/verify_repository.py
verify-kappa:
	$(PYTHON) -B scripts/verify_kappa.py
reproduce:
	$(PYTHON) -B scripts/reproduce_analysis.py
composition:
	$(PYTHON) -B scripts/analyze_corpus_composition.py
figures-conceptual:
	$(PYTHON) -B scripts/regenerate_public_figures.py --conceptual-only
figures-public:
	$(PYTHON) -B scripts/regenerate_public_figures.py
