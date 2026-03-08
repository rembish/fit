VENV   := .venv
PYTHON := $(VENV)/bin/python
PIP    := $(VENV)/bin/pip

.PHONY: help install lint format typecheck test tox pre-commit build twine publish clean distclean

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "  install     set up the virtual environment"
	@echo "  lint        run ruff"
	@echo "  format      run black"
	@echo "  typecheck   run mypy"
	@echo "  test        run pytest with coverage"
	@echo "  tox         run tests across py38, py310, py312"
	@echo "  pre-commit  install pre-commit hooks"
	@echo "  build       build sdist and wheel"
	@echo "  twine       build + check with twine"
	@echo "  publish     upload to PyPI (set TWINE_USERNAME/TWINE_PASSWORD)"
	@echo "  clean       remove build artifacts and caches"
	@echo "  distclean   clean + remove .venv"

$(VENV)/bin/activate: pyproject.toml
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"
	touch $(VENV)/bin/activate

install: $(VENV)/bin/activate
	@echo "Virtual environment ready at $(VENV)/"

lint: $(VENV)/bin/activate
	$(VENV)/bin/ruff check fit tests

format: $(VENV)/bin/activate
	$(VENV)/bin/black fit tests

typecheck: $(VENV)/bin/activate
	$(VENV)/bin/mypy fit

test: $(VENV)/bin/activate
	$(VENV)/bin/pytest --cov=fit --cov-report=term-missing

tox: $(VENV)/bin/activate
	$(VENV)/bin/tox

pre-commit: $(VENV)/bin/activate
	$(VENV)/bin/pre-commit install

build: $(VENV)/bin/activate
	rm -rf dist
	$(PYTHON) -m build

twine: build
	$(VENV)/bin/twine check dist/*

publish: twine
	$(VENV)/bin/twine upload dist/*

clean:
	rm -rf build dist *.egg-info .mypy_cache .ruff_cache .pytest_cache __pycache__
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete

distclean: clean
	rm -rf $(VENV)
