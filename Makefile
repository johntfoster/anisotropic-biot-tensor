PYTHON ?= python3
LATEXMK ?= latexmk

.PHONY: paper site supplement check clean

# Canonical manuscript build; output goes to build/ only.
paper:
	$(LATEXMK) -lualatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex

site:
	$(PYTHON) .agent/shared/tools/research_project.py site

supplement:
	$(PYTHON) tools/package_numerical_supplement.py

check:
	$(PYTHON) .agent/shared/tools/research_project.py check
	tools/agentctl check

clean:
	$(LATEXMK) -C -outdir=build main.tex
