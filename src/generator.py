from .config import Config, load_config_model


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
