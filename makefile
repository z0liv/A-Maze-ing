PYTHON = .venv/bin/python3
DEBUG = python -m pdb
CONFIG = config.txt
FLAKE = flake8
MYPY = mypy . --warn-return-any --warn-unused-ignores \
--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
MYPY_STRICT = mypy . --strict
MAIN = a_maze_ing.py
SRC = src

all: run

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(DEBUG) $(MAIN) $(CONFIG)

install: requirements.txt
	pip install -r requirements.txt

lint: 
	$(FLAKE) $(MAIN) $(SRC) && $(MYPY)

lint-strict:
	$(FLAKE) $(MAIN) $(SRC) && $(MYPY_STRICT) 

clean:
	rm -rf __pycache__ .mypy_cache
	rm -rf src/__pycache__

.PHONY: run install lint lint-strict clean
