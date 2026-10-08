from collections import deque
from random import Random, shuffle
from .errors import InvalidConfigError
from .algorithms import (
    genmaze_ab, genmaze_dfs,
    solve_maze_bfs, active_solution_path,
    get_connected_neighbours, opposite,
    get_not_connected_neighbours, get_neighbours)
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
        If the perfect flag is set to false, calls the function
        that makes the maze imperfect.
        """
        if self.seed is not None and self.use_seed:
            rnd = Random(self.seed)
        else:
            rnd = Random()

        if self.algorithm == "ab":
            self.grid = genmaze_ab(self.grid, self.entry, rnd)
        else:
            self.grid = genmaze_dfs(self.grid, self.entry, rnd)

        if (not self.perfect):
            self.make_imperfect()

        self.solution = solve_maze_bfs(self.grid, self.entry, self.exit)

        active_solution_path(self.solution)
        export_maze(self.grid, self.entry, self.exit,
                    self.output_file, self.solution)

    def make_imperfect(self) -> None:
        """
        Makes the maze imperfect. While the maze has dead-ends, tries to
        remove it, if able, searches for another one, until the remainging
        two dead-ends are left.
        """
        max_pattern_dead_ends = 2
        while True:
            dead_ends = self.get_dead_ends()
            if not dead_ends:
                break
            normal_dead_ends = [
                dead_end for dead_end in dead_ends
                if not dead_end[1]
            ]
            pattern_dead_ends = [
                dead_end for dead_end in dead_ends
                if dead_end[1]
            ]
            if normal_dead_ends:
                candidates = normal_dead_ends
            elif len(pattern_dead_ends) <= max_pattern_dead_ends:
                break
            else:
                candidates = pattern_dead_ends
            removed = False
            for cell, _ in candidates:
                directions = self.get_removable_walls(cell)
                shuffle(directions)
                for direction in directions:
                    if self.remove_wall_if_valid(cell, direction):
                        removed = True
                        break
                if removed:
                    break
            if not removed:
                break

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

    def get_dead_ends(self) -> list[tuple[Cell, bool]]:
        """
        Searches for dead ends in the maze, a dead-end being a cell with only
        one conneted neighbour. It also checks if the dead-end it's part of
        the pattern.

        Returns:
            A list of tuples, each tuple containing the cell that is a dead-end
            and a boolean that tells if it's part of the pattern.
        """
        dead_ends: list[tuple[Cell, bool]] = []

        for row in self.grid:
            for cell in row:
                if cell.is_pattern:
                    continue
                neighbours = get_neighbours(cell, self.grid)
                connected = get_connected_neighbours(cell, self.grid)
                if len(connected) != 1:
                    continue
                pattern_neighbours = sum(
                    neighbour.is_pattern
                    for neighbour, _ in neighbours
                    if neighbour not in [connected[0][0]]
                )
                is_pattern_dead_end = pattern_neighbours == 3
                dead_ends.append((cell, is_pattern_dead_end))
        return dead_ends

    def get_removable_walls(
            self,
            cell: Cell
    ) -> list[DIRECTION]:
        """
        A function that is called when a dead-end is found,
        it checks which of the cell's walls are removable.

        Args:
            cell (Cell): The cell that is a dead-end.
        Returns:
            A list of directions, indicating that the wall of the cell is
            removable in that direction.
        """
        neighbours = get_not_connected_neighbours(cell, self.grid)
        return [
            direction for neighbour, direction in neighbours
            if not neighbour.is_pattern
        ]

    def remove_wall_if_valid(
            self,
            target_cell: Cell,
            direction: DIRECTION
    ) -> bool:
        """
        Checks if the removal of the wall indicated by the given cell and the
        direction is valid.

        Args:
            target_cell (Cell): The target cell from which a wall must be
                                removed.
            direction (DIRECTION): The direction that points the wall that is
                                   going to be checked.
        Returns:
            A boolean that tells if the wall can be removed or not.
        """
        dx, dy = {
            DIRECTION.NORTH: (0, -1),
            DIRECTION.EAST: (1, 0),
            DIRECTION.SOUTH: (0, 1),
            DIRECTION.WEST: (-1, 0),
        }[direction]

        x = target_cell.position[0] + dx
        y = target_cell.position[1] + dy

        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        neighbour = self.grid[y][x]

        target_cell.walls &= ~direction.value
        neighbour.walls &= ~opposite(direction).value

        if check_open_areas(self.grid):
            target_cell.walls |= direction.value
            neighbour.walls |= opposite(direction).value
            return False

        return True


def check_full_conectivity(
        grid: list[list[Cell]],
        entry: Cell,
        pattern: bool,
        height: int,
        width: int
) -> bool:
    """
    Checks if the maze is fully connected, meaning there are no enclosed cells
    or passages. It searches for every reachable cell, until no connected cells
    are left.

    Args:
        grid (list[list[Celll]]): Stores all the cells of the maze.
        entry (Cell): The entry cell
        pattern: (bool): A boolean that indicates if the pattern is active
                         in the maze.
        height (int): The number of rows of the maze.
        width (int): The number of cells in each row of the maze.

    Returns:
        A boolean that tells if it is fully connected or not.
    """
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
    """
    Checks if a 3x3 empty area is created when attempting to remove a wall.

    Args:
        grid (list[list[Cell]]): Stores all the cells of the maze.

    Returns:
        A boolean that indicates if a open area is generated when trying to
        remove the wall.
    """
    for row in grid:
        for cell in row:
            if (cell.walls == 0):
                if check_open_neighbours(grid, cell) == 8:
                    return True
    return False


def check_open_neighbours(grid: list[list[Cell]], cell: Cell) -> int:
    """
    A helper fucntion that checks the disposition of all eight neighbour
    cell's walls.

    Args:
        grid (list[list[Cell]]): Stores all the cells of the maze.
        cell (Cell): The target cell from which the neighbours are cheked.

    Returns:
        The count of neighbour cells that are correctly disposed to form a
        3x3 empty area.
    """
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
