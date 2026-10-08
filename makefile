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
SRC = config.py enums.py rendering.py theme.py

all: run

run: create-venv install
	clear
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(DEBUG) $(MAIN) $(CONFIG)

install: create-venv requirements.txt
	$(PYTHON) -m pip install -r requirements.txt
	$(PIP) install dist/mlx-2.4-py3-none-any.whl
	$(PIP) install dist/mazegen-1.0.0-py3-none-any.whl

lint: install
	$(FLAKE) $(MAIN) $(SRC) && $(MYPY)

lint-strict: install
	$(FLAKE) $(MAIN) $(SRC) && $(MYPY_STRICT) 

clean:
	rm -rf .venv
	find . -type d \( -name "__pycache__" -o -name ".mypy_cache" \) -exec rm -rf {} +

create-venv:
	python3 -m venv .venv

.PHONY: run install lint lint-strict clean
