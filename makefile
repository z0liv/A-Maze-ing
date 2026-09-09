PYTHON = python3
CONFIG = config.txt
FLAKE = flake8 -v
MYPY = mypy . --warn-return-any --warn-unused-ignores \
--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
MYPY_STRICT = mypy . --strict
MAIN = a_maze_ing.py

all: run

run:
	$(PYTHON) $(MAIN) $(CONFIG)

lint: 
	$(FLAKE) && $(MYPY)

lint-strict:
	$(FLAKE) && $(MYPY_STRICT)

clean:
	rm -rf __pycache__ .mypy_cache
