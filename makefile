PYTHON = python3
MAIN = a_maze_ing.py
CONFIG = config.txt

all: run

run:
	$(PYTHON) $(MAIN) $(CONFIG)

clean:
	rm -rf __pycache__