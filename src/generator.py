from .config import Config, load_config_model
from .errors import InvalidConfigError


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
    is_pattern: bool
    is_entry: bool
    is_exit: bool

    def __init__(
            self, position: tuple[int, int],
            walls: int, visited: bool,
            is_pattern: bool, is_entry: bool,
            is_exit: bool
    ) -> None:
        """
        Initialize the cell with the attributes defined previously.
        """
        self.position = position
        self.walls = walls
        self.visited = visited
        self.is_pattern = is_pattern
        self.is_entry = is_entry
        self.is_exit = is_exit


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
    has_pattern: bool = False
    use_seed: bool

    def __init__(self) -> None:
        """
        Initialize the maze.

        We do the config file parsing here.
        """
        self.config = load_config_model()
        self.grid = generate_grid(self.config)
        if self.config.width >= 8 and self.config.height >= 6:
            self.has_pattern = True
        if self.has_pattern:
            pattern_pos = pattern_positions(calculate_center(self.grid))
            define_pattern(self.grid)
            msgs: list[str] = list()

            if self.config.entry in pattern_pos:
                entry: str = "ENTRY" + str(self.config.entry)
                msgs.append(entry + " cannot be part of the pattern")
            if self.config.entry in pattern_pos:
                exit: str = "EXIT" + str(self.config.exit)
                msgs.append(exit + " cannot be part of the pattern")
            if len(msgs) > 0:
                raise InvalidConfigError(msgs)

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
            if x == config.entry[0] and y == config.entry[1]:
                cell = Cell((x, y), 15, False, False, True, False)
            elif x == config.exit[0] and y == config.exit[1]:
                cell = Cell((x, y), 15, False, False, False, True)
            else:
                cell = Cell((x, y), 15, False, False, False, False)
            row.append(cell)
        grid.append(row)
    return grid


def define_pattern(grid: list[list[Cell]]) -> None:
    center: tuple[int, int] = calculate_center(grid)
    for row in grid:
        for cell in row:
            if cell.position in pattern_positions(center):
                cell.is_pattern = True
                cell.visited = True


def calculate_center(grid: list[list[Cell]]) -> tuple[int, int]:
    center: tuple[int, int]
    width: int = len(grid[0])
    height: int = len(grid)
    if height % 2 == 1 and width % 2 == 1:
        center = (width // 2, height // 2)
    elif height % 2 == 0 and width % 2 == 1:
        center = (width // 2, height // 2 - 1)
    elif height % 2 == 1 and width % 2 == 0:
        center = (width // 2 - 1, height // 2)
    else:
        center = (width // 2 - 1, height // 2 - 1)
    return center


def pattern_positions(center: tuple[int, int]) -> list[tuple[int, int]]:
    x, y = center
    pattern_pos: list[tuple[int, int]] = [
        (x - 3, y - 2), (x - 3, y - 1), (x - 3, y), (x - 2, y),
        (x - 1, y), (x - 1, y + 1), (x - 1, y + 2), (x + 1, y - 2),
        (x + 2, y - 2), (x + 3, y - 2), (x + 3, y - 1), (x + 3, y),
        (x + 2, y), (x + 1, y), (x + 1, y + 1), (x + 1, y + 2),
        (x + 2, y + 2), (x + 3, y + 2)]
    return pattern_pos
