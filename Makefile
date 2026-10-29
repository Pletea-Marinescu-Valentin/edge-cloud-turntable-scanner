# Rebuilds every figure and the PDF of the paper. Each target calls scripts/build.py,
# which also works without make (python scripts/build.py <target>).
#   make figures   Python figures -> paper/figs/ (TikZ figures are compiled with the paper)
#   make paper     paper/main.pdf with latexmk
#   make check     citation, page, word and repository checks
#   make dist      dist/edge-cloud-turntable-scanner.pdf and dist/overleaf.zip
#   make all       all of the above, in this order

PYTHON ?= python

.PHONY: all figures paper check dist clean

all:
	$(PYTHON) scripts/build.py all

figures paper check dist:
	$(PYTHON) scripts/build.py $@

clean:
	cd paper && latexmk -C main.tex
	rm -rf dist
