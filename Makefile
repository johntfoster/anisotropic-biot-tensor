PYTHON ?= python3
LATEXMK ?= latexmk

.PHONY: paper site supplement figures check clean

# Canonical manuscript build; output goes to build/ only.
paper:
	$(LATEXMK) -lualatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex

site:
	$(PYTHON) .agent/shared/tools/research_project.py site

supplement:
	$(PYTHON) tools/package_numerical_supplement.py

# Regenerate the contour evidence, then the figures and manifest that hash it,
# then re-verify every declared digest. Order matters: the decks rewrite the
# Exodus files the plot manifest hashes.
figures:
	$(PYTHON) tools/rerun_fabric_contours.py
	$(PYTHON) tools/check_figure_manifests.py

check:
	$(PYTHON) .agent/shared/tools/research_project.py check
	tools/agentctl check

clean:
	$(LATEXMK) -C -outdir=build main.tex
