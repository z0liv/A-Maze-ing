VENV = .venv/bin
PYTHON = ${VENV}/python3
PIP = ${VENV}/pip
DEBUG = ${PYTHON} -m pdb
CONFIG = config.txt
FLAKE = ${VENV}/flake8
MYPY = ${VENV}/mypy . --warn-return-any --warn-unused-ignores \
--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
MYPY_STRICT = ${VENV}/mypy . --strict
MAIN = a_maze_ing.py
SRC = config.py enums.py rendering.py theme.py mazegen

all: run

run: install
	clear
	$(PYTHON) $(MAIN) $(CONFIG)

build: create-venv
	rm -rf dist
	$(PYTHON) -m build
	cp dist/*.whl .
	cp dist/*.tar.gz .

debug: install
	$(DEBUG) $(MAIN) $(CONFIG)

install: create-venv requirements.txt
	$(PYTHON) -m pip install -r requirements.txt
	$(MAKE) build
	$(PIP) install mlx-2.4-py3-none-any.whl
	$(PIP) install mazegen-1.0.0-py3-none-any.whl

lint: install
	$(FLAKE) $(MAIN) $(SRC) && $(MYPY)

lint-strict: install
	$(FLAKE) $(MAIN) $(SRC) && $(MYPY_STRICT) 

clean:
	rm -rf .venv
	rm -rf *.egg-info
	rm -rf dist
	rm -rf mazegen/*.egg-info
	rm -rf mazegen-1.0.0-py3-none-any.whl
	rm -rf mazegen-1.0.0.tar.gz
	find . -type d \( -name "__pycache__" -o -name ".mypy_cache" \) -exec rm -rf {} +

create-venv:
	python3 -m venv .venv

.PHONY: run install lint lint-strict clean build debug
