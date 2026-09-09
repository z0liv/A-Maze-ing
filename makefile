PYTHON = python3
MAIN = a_maze_ing.py

all: run

run:
	$(PYTHON) $(MAIN)

clean:
	rm -rf __pycache__
