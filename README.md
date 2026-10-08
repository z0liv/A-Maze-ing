*This project has been created as part of the 42 curriculum by jrecio-t, omarquez.*

# A-Maze-ing

## Description

**A-Maze-ing** is a Python maze generator with a graphical interface built with MiniLibX (`mlx`). It creates a maze from a configuration file, displays it in a window, calculates a shortest route between the entry and exit, and exports the maze to a text file.

The project is split into two parts:

- **`mazegen`** is a reusable Python package for generating, solving, inspecting, and exporting mazes. It can be used independently of the graphical application.
- **The application and renderer** load the configuration, create the maze, and provide interactive visualization options.

### Features

- Generate mazes with **Aldous–Broder** or **Depth-First Search (DFS)**.
- Choose between perfect and imperfect mazes.
- Set maze dimensions, entry and exit coordinates, and output filename.
- Use a seed to make generation reproducible.
- Find a shortest path with **Breadth-First Search (BFS)** and animate it in the graphical view.
- Regenerate a maze, switch visual themes, and swap wall/background colours.
- Export the maze as a text file.
- Reuse the `mazegen` wheel in other Python projects.

## Instructions

### Requirements

- Python **3.10 or newer**.
- A graphical environment supported by the project's `mlx` / MiniLibX package.
- The dependencies in `requirements.txt`.
- The local wheel files expected by the supplied Makefile: `dist/mlx-2.4-py3-none-any.whl` and `dist/mazegen-1.0.0-py3-none-any.whl`.

On Linux, a working display server is required. On WSL, ensure WSLg or another supported X/Wayland configuration is functioning before starting the application.

### Installation

From the repository root, install the project dependencies and local wheels using:

```bash
make install
```

The Makefile expects the two wheel files listed above to exist in `dist/`. If they are not provided in your checkout, build or obtain them before using the corresponding Makefile targets.

To build the reusable `mazegen` wheel from the package directory, install the build frontend if necessary and run:

```bash
python3 -m pip install build
python3 -m build --wheel
```

Run this from the directory containing `pyproject.toml` and the `mazegen/` package. The generated wheel is written to `dist/`.

### Run the application

Use the default configuration:

```bash
make run
```

Or provide a configuration file explicitly:

```bash
.venv/bin/python3 a_maze_ing.py config.txt
```

The application expects one command-line argument: the path to the configuration file. When generation succeeds, the maze is exported to the configured output file and opened in the graphical window.

### Keyboard controls

| Key | Action |
| --- | --- |
| `1` | Generate another maze. |
| `2` | Start or stop the solution-path animation; press again to reset after completion. |
| `3` | Swap the background and wall colours. |
| `4` | Cycle through the available themes. |
| `5` | Close the application. |

The numeric keypad equivalents are supported as well.

## Configuration file

The application reads a plain-text configuration file. Each setting uses the form `KEY=VALUE`, one per line. Keys are case-insensitive; blank lines and lines starting with `#` are ignored. Do not surround values with quotes. `ENTRY` and `EXIT` use `x,y` coordinates, with `(0, 0)` at the top-left of the maze.

### Complete example

```ini
WIDTH=15
HEIGHT=14
ENTRY=14,9
EXIT=1,1
PERFECT=False
OUTPUT_FILE=maze.txt
#SEED=42
# Available algorithms: Aldous-Broder (ab), Depth-First Search (dfs)
ALGORITHM=ab
```

### Configuration options

| Key | Format | Meaning and constraints |
| --- | --- | --- |
| `WIDTH` | Integer | Maze width in cells. Must be between `2` and `34`. |
| `HEIGHT` | Integer | Maze height in cells. Must be between `2` and `14`. |
| `ENTRY` | `x,y` | Entry coordinates. Both coordinates must be non-negative and inside the configured maze. |
| `EXIT` | `x,y` | Exit coordinates. Must be inside the maze and different from `ENTRY`. |
| `PERFECT` | `True` or `False` | Whether to generate a perfect maze. Defaults to `False`. A perfect maze has exactly one path between any two cells; an imperfect maze may contain loops. |
| `OUTPUT_FILE` | Filename/path string | Destination for the exported maze. Defaults to `output_maze.txt`; the configured value is limited to 25 characters by validation. |
| `SEED` | Optional integer | Seed for reproducible generation. Must be at least `1`. Uncomment and set it to enable seeded generation; omit or comment it out for unseeded generation. |
| `ALGORITHM` | `ab` or `dfs` | Maze-generation algorithm. Defaults to `ab` (Aldous–Broder). |

The parser splits each setting at the first `=`. The configuration is validated before generation; invalid syntax, dimensions, coordinates, or incompatible entry/exit positions cause a configuration error.

## Maze-generation and solving algorithms

Two generation algorithms are available:

- **Aldous–Broder (`ab`, default):** performs a random walk through the grid. When the walk first reaches an unvisited cell, it connects that cell to the previously visited cell. Continuing until all cells have been visited produces a spanning tree, and therefore a perfect maze. It is conceptually simple and gives each spanning tree equal probability, although it can take a long time to visit every cell in larger grids.
- **Depth-First Search (`dfs`):** explores unvisited neighbours and backtracks when it reaches a dead end. This is efficient and straightforward to implement, and produces a perfect maze when used without the later modifications for imperfect generation. Its paths often have a more winding, corridor-like appearance.

The default is **Aldous–Broder**, while DFS is available as an alternative so the user can compare the results. The project keeps generation separate from rendering, making it possible to change the generation algorithm without rewriting the graphical view.

**BFS (Breadth-First Search)** is used after generation to find a shortest route from the entry to the exit. Since movement between adjacent cells has equal cost, BFS finds a path with the fewest cell-to-cell moves. The resulting ordered list of cells is used by the application to animate the solution.

When `PERFECT=False`, the generator supports imperfect-maze generation by introducing additional openings while maintaining connectivity. This creates alternative routes and loops rather than a single unique route. A seed allows the same configuration and algorithm to reproduce the same generation sequence.

## Reusable code: the `mazegen` package

The `mazegen` package is deliberately separated from the graphical interface. It can be installed as a wheel and imported into another Python project, command-line tool, or visualization layer.

### Install and import

```bash
python3 -m pip install dist/mazegen-1.0.0-py3-none-any.whl
```

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=10,
    height=10,
    entry=(0, 0),
    exit=(9, 9),
    output_file="maze.txt",
    use_seed=True,
    seed=42,
    perfect=True,
    algorithm="ab",
)

print(f"Maze size: {maze.width} x {maze.height}")
print("Entry:", maze.entry.position)
print("Exit:", maze.exit.position)

for cell in maze.solution:
    print(cell.position)
```

Creating a `MazeGenerator` instance generates the maze, calculates the solution, and exports the result. The main attributes are:

- `maze.grid`: two-dimensional list of `Cell` objects, accessed as `maze.grid[y][x]`.
- `maze.entry` and `maze.exit`: entry and exit `Cell` objects.
- `maze.solution`: shortest path as an ordered list of cells, from entry to exit.
- `cell.position`: cell coordinates as `(x, y)`.
- `cell.walls`: a bitmask representing the cell's walls.

The `DIRECTION` enum exposes `NORTH`, `EAST`, `SOUTH`, and `WEST` for working with wall directions.

### Public API

The package exports the following main components:

- `MazeGenerator` — generates a maze, computes its solution, and exports the result.
- `Cell` — represents a cell and its position/walls.
- `DIRECTION` — cardinal wall directions.
- `genmaze_ab` and `genmaze_dfs` — generation algorithms.
- `solve_maze_bfs` — shortest-path solver.
- `export_maze` — maze export function.
- `ParamsError` and `InvalidConfigError` — parameter and configuration exceptions.

### Package layout

```text
mazegen/
├── __init__.py
├── generator.py
├── cell.py
├── enums.py
├── aldous_broder.py
├── depth_first_search.py
├── breadth_first_search.py
├── alg_utils.py
├── config.py
├── errors.py
├── export.py
└── README.md
```

The library has no dependency on the graphical renderer: other projects can reuse maze generation, solving, cell data, and export functionality without opening a window.

## Teamwork and project management

### Team and roles

The project was developed by **jrecio-t** and **omarquez**. The supplied commit history shows work across the generator, rendering, configuration, interactive controls, validation, documentation, and packaging. Since the provided log excerpt does not associate each commit with an author, the division below describes the main workstreams rather than claiming an exact per-person commit count.

- **Maze algorithms and reusable library:** implementation and integration of Aldous–Broder, DFS, BFS, cell/wall utilities, perfect/imperfect maze handling, seed reproducibility, and text export.
- **Graphical interface and interaction:** MiniLibX rendering, grid and wall drawing, entry/exit display, solution-path visualization and animation, themes, colour switching, regeneration, and application shutdown.
- **Configuration and reliability:** configuration model and parsing, validation and error handling, command-line argument handling, and fixes for rendering and generation edge cases.
- **Code quality and distribution:** docstrings, linting and strict type checking, Makefile improvements, separation of `mazegen` from the UI, and building a distributable wheel with its own README.

These workstreams overlap: the commit history contains integration merges and fixes that touch more than one component. For an exact individual attribution, consult the full Git log with author metadata.

### Planning and how it evolved

The history indicates an iterative development process:

1. **Core generator and configuration:** establish configuration parsing, parameter validation, the `Cell` and generator abstractions, and the initial generation algorithms.
2. **Graphical rendering:** build the grid and wall renderer, then refine cell borders, corners, margins, entry/exit drawing, and rendering performance.
3. **Interactive features:** add regeneration, themes and colour switching, the solution algorithm, and solution animation.
4. **Algorithm and reliability improvements:** add seed handling and reproducibility, support perfect/imperfect mazes, investigate dead ends and open areas, and fix edge cases found while integrating generation with rendering.
5. **Refactoring and delivery:** separate the reusable `mazegen` package from the view, improve docstrings and strict linting, and configure wheel packaging with package documentation.

The plan therefore evolved from proving the basic generation and display pipeline to building a usable interactive application, then improving correctness, maintainability, and reuse.

### What worked well and what could be improved

**What worked well**

- Separating `mazegen` from the renderer made the algorithmic code reusable and easier to document independently.
- Supporting multiple generation algorithms made the project easier to experiment with and compare.
- Seeds helped investigate bugs and reproduce a particular maze during debugging.
- Iterative rendering fixes and lint/type-checking work improved consistency and maintainability.
- The commit history shows that integration and edge cases were addressed throughout development rather than only at the end.

**What could be improved**

- Agreeing on module boundaries and public interfaces earlier could reduce integration fixes and overlapping changes.
- A written task board with owners, estimates, and milestones would make the plan and individual responsibilities clearer.
- Automated tests for generation invariants, entry-to-exit reachability, perfect-maze properties, seed reproducibility, and exported-file formatting would catch regressions earlier.
- GUI testing should include documented display-environment requirements and repeatable manual test steps.
- Commit messages and merge practices could consistently identify the scope of a change, making retrospective contribution tracking easier.

### Tools used

- **Python** for the application and algorithms.
- **MiniLibX / `mlx`** for graphical rendering and keyboard interaction.
- **Pydantic** for configuration validation.
- **Git and GitHub** for version control and collaboration.
- **Make** for installation, execution, cleanup, and quality-check commands.
- **flake8** for style checks and **mypy** for static type checking, including strict checks.
- **Python build tooling (`build` / setuptools)** for packaging `mazegen` as a wheel.

## Development commands

The Makefile provides project shortcuts, including:

```bash
make install       # Create the virtual environment and install dependencies/wheels
make run           # Launch the application with config.txt
make lint          # Run style and type checks
make lint-strict   # Run stricter type checks
make clean         # Remove the virtual environment and Python caches
```

The install and quality-check targets rely on the local wheels described in the installation section.

## Resources and acknowledgements

### References

- [Python documentation](https://docs.python.org/3/)
- [Pydantic documentation](https://docs.pydantic.dev/)
- [Setuptools documentation](https://setuptools.pypa.io/)
- [Python Packaging User Guide — packaging projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Aldous–Broder algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Aldous-Broder_algorithm)
- [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search)
- [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)
- [MiniLibX](https://github.com/42Paris/minilibx-linux) (Linux implementation reference)

### Use of AI

AI assistance was used as a supporting tool during development and documentation. It was used to help explain and review algorithmic approaches (including DFS and BFS), reason about maze-generation and rendering bugs, discuss Python implementation details, and improve documentation and README structure. AI suggestions were treated as guidance: implementation choices and project-specific behaviour were checked against the code and adapted to the project. AI was not a substitute for understanding, integrating, or validating the submitted work.

## Authors

- **jrecio-t**
- **omarquez**

The `mazegen` package is distributed under the MIT License; see `LICENSE.md` in the repository.
