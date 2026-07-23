.PHONY: install test lint gradient-check smoke paper clean
install:
	python -m pip install -e '.[dev]'
test:
	pytest
gradient-check:
	python scripts/validate_gradients.py
smoke:
	python scripts/reproduce_all.py --profile smoke
paper:
	cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex && cp main.pdf manuscript.pdf
lint:
	ruff check src tests scripts
clean:
	rm -rf .pytest_cache .ruff_cache build dist *.egg-info results/generated/*
	cd paper && latexmk -C main.tex
