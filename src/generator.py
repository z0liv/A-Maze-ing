import sys
import random
from .config import Config
from .errors import InvalidConfigError, ParamsError
from .enums import DIRECTION
from typing import Any
from pydantic import ValidationError


class Cell:
    """
    Class that represents each cell of the maze.

    Attributes:
        position (tuple[int, int]): Defines the location of the cell in a tuple
                                    of x, y coordinates.
        walls: (int): A integer that determines which walls are present.
        visited: (bool): A boolean that tells if
                         the cell is part of the solution(s).
    """
    position: tuple[int, int]
    walls: int
    visited: bool

    def __init__(
            self, position: tuple[int, int],
            walls: int, visited: bool
    ) -> None:
        """
        Initialize the cell with the attributes defined previously.
        """
        self.position = position
        self.walls = walls
        self.visited = visited


class MazeGenerator:
    """
    Class that will generate the maze.

    Attributes:
        config (Config): It stores all the info gathered from the config file.
        entry: (Cell): Indicates which cell is the entrance of the maze.
        exit: (Cell): Indicates which cell is the exit of the maze.
    """
    config: Config
    grid: list[list[Cell]]
    entry: Cell
    exit: Cell

    def __init__(self) -> None:
        """
        Initialize the maze.

        We do the config file parsing here.
        """
        self.config = load_config_model()
        self.grid = generate_grid(self.config)

        entry_x, entry_y = self.config.entry
        exit_x, exit_y = self.config.exit

        self.entry = self.grid[entry_y][entry_x]
        self.exit = self.grid[exit_y][exit_x]

        self.entry.visited = True

def generate_grid(config: Config) -> list[list[Cell]]:
    """
        Generate the grid of cells that will be used to create the maze.

        Args:
            config (Config): The configuration model that contains the
                information about the maze.

        Returns:
            A 2D list of Cell objects that represents the grid of cells.
    """
    grid: list[list[Cell]] = []
    for y in range(config.height):
        row: list[Cell] = []
        for x in range(config.width):
            cell = Cell((x, y), 15, False)
            row.append(cell)
        grid.append(row)
    return grid

def get_neighbors(cell: Cell, grid: list[list[Cell]]) -> list[tuple[Cell, DIRECTION]]:
    """
        Get the neighbors of a given cell in the grid.

        Args:
            cell (Cell): The cell for which to find neighbors.
            grid (list[list[Cell]]): The grid of cells.

        Returns:
            A list of neighboring Cell objects.
    """
    x, y = cell.position
    neighbors: list[tuple[Cell, DIRECTION]] = []

    # Check the four cardinal directions
    if y > 0:  # North
        neighbors.append((grid[y - 1][x], DIRECTION.NORTH))
    if x < len(grid[0]) - 1:  # East
        neighbors.append((grid[y][x + 1], DIRECTION.EAST))
    if y < len(grid) - 1:  # South
        neighbors.append((grid[y + 1][x], DIRECTION.SOUTH))
    if x > 0:  # West
        neighbors.append((grid[y][x - 1], DIRECTION.WEST))

    return neighbors


def generate_maze_ab(maze_generator: MazeGenerator) -> None:
    """
        Generate the maze using the Aldous-Broder algorithm.

        Args:
            maze_generator (MazeGenerator): The maze generator instance.
    """
    width = maze_generator.config.width
    height = maze_generator.config.height
    current_cell = maze_generator.entry
    visited_cells = 1
    total_cells = width * height

    while visited_cells < total_cells:
        neighbors = get_neighbors(current_cell, maze_generator.grid)
        next_cell, direction = random.choice(neighbors)

        if not next_cell.visited:
            current_cell.walls &= ~direction.value
            next_cell.walls &= ~opposite(direction).value
            next_cell.visited = True
            visited_cells += 1

        current_cell = next_cell


def opposite(direction: DIRECTION) -> DIRECTION:
    """
        Get the opposite direction of a given direction.

        Args:
            direction (DIRECTION): The direction for which to find the opposite.

        Returns:
            The opposite DIRECTION.
    """
    if direction == DIRECTION.NORTH:
        return DIRECTION.SOUTH
    elif direction == DIRECTION.EAST:
        return DIRECTION.WEST
    elif direction == DIRECTION.SOUTH:
        return DIRECTION.NORTH
    elif direction == DIRECTION.WEST:
        return DIRECTION.EAST
    else:
        raise ValueError("Invalid direction")

def validate_params() -> str:
    """
        Validate that there is the correct number of params.

        Returns:
            The filename extracted from the sys.argv.
        Raises:
            ParamsError: If the number of params is equal to 1 or
                is greater than 2.
    """
    try:
        args = sys.argv
        if len(args) == 1:
            prefix = "Missing config file"
            raise ParamsError(prefix + ", expected 'config.txt'")
        elif len(args) > 2:
            prefix = "Too many params, "
            raise ParamsError(
                prefix + f"expected 1 received {len(args) - 1}"
                )
        return args[1]
    except Exception:
        raise


def load_config_model() -> Config:
    """
        Reads the configuration file and loads its values
        into the Config model.

        Raises:
            ValueError: If the syntax of the config file is not "key=value".
            InvalidConfigError: If the configuration fails model validation.
    """
    try:
        filename = validate_params()
        data: dict[str, Any] = {}
        with open(filename, "r") as config_file:
            for line in config_file:
                line = line.strip()
                if len(line) > 0:
                    if line[0] == "#":
                        continue
                else:
                    continue
                try:
                    key, value = line.split("=", 1)
                    if (key.lower() == "entry" or key.lower() == "exit"):
                        lst_value = (value.split(","))
                        data[key.lower()] = lst_value
                    else:
                        data[key.lower()] = value
                except ValueError:
                    prefix: str = "[ERROR] The configuration file"
                    raise ValueError(prefix + " must have 'key=value' syntax")
        config_model: Config = Config(**data)
        return config_model
    except ValidationError as val:
        errors: list[str] = []
        for error in val.errors():
            if len(error.get("loc")) != 0 and error.get("type") == "missing":
                prefix = error.get("msg") + ": '"
                errors.append(prefix + str(error.get("loc")[0]).upper() + "'")
            elif len(error.get("loc")) != 0:
                prefix = "'" + str(error.get("loc")[0]).upper()
                errors.append(prefix + "' " + error.get("msg"))
            else:
                errors.append(error.get("msg"))
        raise InvalidConfigError(errors)
