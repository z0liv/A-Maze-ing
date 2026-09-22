VENV = .venv/bin
PYTHON = ${VENV}/python3
DEBUG = ${PYTHON} -m pdb
CONFIG = config.txt
FLAKE = ${VENV}/flake8
MYPY = ${VENV}/mypy . --warn-return-any --warn-unused-ignores \
--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
MYPY_STRICT = ${VENV}/mypy . --strict
MAIN = a_maze_ing.py
SRC = src

all: run

run: create-venv install
	clear
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(DEBUG) $(MAIN) $(CONFIG)

install: requirements.txt
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install mlx-2.4-py3-none-any.whl

lint: 
	$(FLAKE) $(MAIN) $(SRC) && $(MYPY)

lint-strict:
	$(FLAKE) $(MAIN) $(SRC) && $(MYPY_STRICT) 

clean:
	rm -rf .venv
	find . -type d \( -name "__pycache__" -o -name ".mypy_cache" \) -exec rm -rf {} +

create-venv:
	python3 -m venv .venv

.PHONY: run install lint lint-strict clean
