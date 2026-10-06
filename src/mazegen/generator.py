from collections import deque
from random import Random
from .errors import InvalidConfigError
from .algorithms import (
    genmaze_ab, genmaze_dfs,
    solve_maze_bfs, active_solution_path,
    get_connected_neighbours, opposite)
from .cell import Cell
from .export import export_maze
from .enums import DIRECTION


class MazeGenerator:
    """
    Class that will generate the maze.

    Attributes:
        width (int): The width of the maze.
        height (int): The height of the maze.
        entry_pos (tuple[int, int]): Tuple that represents the x, y position
                                    of the entry of the maze.
        exit_pos (tuple[int, int]): Tuple that represents the x, y position
                                    of the exit of the maze.
        use_seed (bool): Indicates if the maze it's going to be
                        generated via seed.
        perfect (bool): Indicates if the generated maze it's going to be
                        perfect or imperfect.
        algorithm (str): String to select an specific algorithm to generate
                        the maze.
        grid (list[list[Cell]]): Represents a 2D list of Cells.
        entry (Cell): Indicates which cell is the entrance of the maze.
        exit (Cell): Indicates which cell is the exit of the maze.
        has_pattern (bool): Indicates if the grid is big enough to have a
                            '42' pattern inside.
        seed (int): An integer to reproduce an specific maze.
    """
    entry: Cell
    exit: Cell
    grid: list[list[Cell]]
    has_pattern: bool = False

    def __init__(
            self, width: int, height: int,
            entry: tuple[int, int], exit: tuple[int, int],
            output_file: str,
            use_seed: bool,
            perfect: bool = False,
            seed: int | None = None,
            algorithm: str = "ab",
    ) -> None:
        """
        Initialize the maze generating the grid, using an algoritm to
        generate a maze, store the solution path and exporting it.
        """

        self.width = width
        self.height = height
        self.entry_pos = entry
        self.exit_pos = exit
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed
        self.algorithm = algorithm
        self.use_seed = use_seed

        self.grid = self.generate_grid()

        if self.width >= 8 and self.height >= 6:
            self.has_pattern = True
        if self.has_pattern:
            pattern_pos = pattern_positions(calculate_center(self.grid))
            define_pattern(self.grid)
            msgs: list[str] = list()

            if self.entry_pos in pattern_pos:
                entry_msg = "ENTRY " + str(self.entry_pos)
                msgs.append(entry_msg + " cannot be inside of the pattern")
            if self.exit_pos in pattern_pos:
                exit_msg = "EXIT " + str(self.exit_pos)
                msgs.append(exit_msg + " cannot be inside of the pattern")
            if len(msgs) > 0:
                raise InvalidConfigError(msgs)

        entry_x, entry_y = self.entry_pos
        exit_x, exit_y = self.exit_pos

        self.entry = self.grid[entry_y][entry_x]
        self.exit = self.grid[exit_y][exit_x]

        self.entry.visited = True
        self.generate()

    def generate(self) -> None:
        """
        Helper function to generate the maze based on the selected
        algorithm, store the solution path and exporting it.
        """
        if self.seed is not None and self.use_seed:
            rnd = Random(self.seed)
        else:
            rnd = Random()

        if self.algorithm == "ab":
            self.grid = genmaze_ab(self.grid, self.entry, rnd)
        else:
            self.grid = genmaze_dfs(self.grid, self.entry, rnd)
        self.solution = solve_maze_bfs(self.grid, self.entry, self.exit)

        active_solution_path(self.solution)
        export_maze(self.grid, self.entry, self.exit,
                    self.output_file, self.solution)

    def generate_grid(self) -> list[list[Cell]]:
        """
        Generate the grid of cells that will be used to create the maze.

        Returns:
            A 2D list of Cell objects that represents the grid of cells.
        """
        grid: list[list[Cell]] = []
        for y in range(self.height):
            row: list[Cell] = []
            for x in range(self.width):
                if x == self.entry_pos[0] and y == self.entry_pos[1]:
                    cell = Cell((x, y), 15, False, False, True, False)
                elif x == self.exit_pos[0] and y == self.exit_pos[1]:
                    cell = Cell((x, y), 15, False, False, False, True)
                else:
                    cell = Cell((x, y), 15, False, False, False, False)
                row.append(cell)
            grid.append(row)
        return grid

    def remove_wall(
            self,
            target_cell: Cell,
            direction: DIRECTION
    ) -> None:
        if check_open_areas(self.grid):
            target_cell.walls &= ~direction.value
            dx, dy = {
                DIRECTION.NORTH: (0, -1),
                DIRECTION.EAST: (1, 0),
                DIRECTION.SOUTH: (0, 1),
                DIRECTION.WEST: (-1, 0),
            }[direction]
            neighbour: Cell = self.grid[target_cell.position[1] + dy][target_cell.position[0] + dx]
            neighbour.walls &= ~opposite(direction).value

def check_full_conectivity(
        grid: list[list[Cell]],
        entry: Cell,
        pattern: bool,
        height: int,
        width: int
) -> bool:
    seen: set[Cell] = {entry}
    queue: deque[Cell] = deque([entry])
    while queue:
        current: Cell = queue.popleft()
        connected: list[Cell] = [x[0] for x in
                                 get_connected_neighbours(current, grid)]
        for next in connected:
            if next not in seen:
                seen.add(next)
                queue.append(next)
    if (pattern and len(seen) == height * width - 18):
        return True
    elif (not pattern and len(seen) == height * width):
        return True
    else:
        return False


def check_open_areas(grid: list[list[Cell]]) -> bool:
    for row in grid:
        for cell in row:
            if (cell.walls == 0):
                if check_open_neighbours(grid, cell) == 8:
                    return True
    return False


def check_open_neighbours(grid: list[list[Cell]], cell: Cell) -> int:
    x, y = cell.position
    count: int = 0
    # North
    if y > 0 and grid[y - 1][x].walls == 1:
        count += 1
    # East
    if x < len(grid[0]) - 1 and grid[y][x + 1].walls == 2:
        count += 1
    # South
    if y < len(grid) - 1 and grid[y + 1][x].walls == 4:
        count += 1
    # West
    if x > 0 and grid[y][x - 1].walls == 8:
        count += 1
    # North-West
    if x > 0 and y > 0 and grid[y - 1][x - 1].walls == 9:
        count += 1
    # North-East
    if x < len(grid[0]) - 1 and y > 0 - 1 and grid[y - 1][x + 1].walls == 3:
        count += 1
    # South-West
    if x > 0 and y < len(grid) - 1 and grid[y + 1][x - 1].walls == 12:
        count += 1
    # South-East
    if (x < len(grid[0]) - 1 and y < len(grid) - 1
            and grid[y + 1][x + 1].walls == 10):
        count += 1
    return count


def define_pattern(grid: list[list[Cell]]) -> None:
    """
    Calls a function that calculates the grid's center and checks every cell to
    alter some of it' values.

    Args:
        grid: The data structure that stores all the cells.
    """
    center: tuple[int, int] = calculate_center(grid)
    for row in grid:
        for cell in row:
            if cell.position in pattern_positions(center):
                cell.is_pattern = True
                cell.visited = True


def calculate_center(grid: list[list[Cell]]) -> tuple[int, int]:
    """
    Calculates the center of the grid depending on the parity of the number of
    cells per row and column.

    Args:
        grid: The data structure that stores all the cells.

    Returns:
        A pair of x,y values that represent the chosen center cell of the grid.
    """
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
    """
    Calculates and stores all the cells that belong to the pattern
    Args:
        center: A pair of x, y values that represent the center.
    Returns:
        A list of the selected cells
    """
    x, y = center
    pattern_pos: list[tuple[int, int]] = [
        (x - 3, y - 2), (x - 3, y - 1), (x - 3, y), (x - 2, y),
        (x - 1, y), (x - 1, y + 1), (x - 1, y + 2), (x + 1, y - 2),
        (x + 2, y - 2), (x + 3, y - 2), (x + 3, y - 1), (x + 3, y),
        (x + 2, y), (x + 1, y), (x + 1, y + 1), (x + 1, y + 2),
        (x + 2, y + 2), (x + 3, y + 2)]
    return pattern_pos
