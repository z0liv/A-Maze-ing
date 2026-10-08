from . import Cell
from .enums import DIRECTION


def get_neighbours(
        cell: Cell,
        grid: list[list[Cell]]
) -> list[tuple[Cell, DIRECTION]]:
    """
    Get the neighbours of a given cell in the grid.

    Args:
        cell (Cell): The cell for which to find neighbours.
        grid (list[list[Cell]]): The grid of cells.

    Returns:
        A list of neighboring Cell objects.
    """
    x, y = cell.position
    neighbours: list[tuple[Cell, DIRECTION]] = []

    # Check the four cardinal directions
    if y > 0 and not grid[y - 1][x].is_pattern:  # North
        neighbours.append((grid[y - 1][x], DIRECTION.NORTH))
    if x < len(grid[0]) - 1 and not grid[y][x + 1].is_pattern:  # East
        neighbours.append((grid[y][x + 1], DIRECTION.EAST))
    if y < len(grid) - 1 and not grid[y + 1][x].is_pattern:  # South
        neighbours.append((grid[y + 1][x], DIRECTION.SOUTH))
    if x > 0 and not grid[y][x - 1].is_pattern:  # West
        neighbours.append((grid[y][x - 1], DIRECTION.WEST))

    return neighbours


def get_unvisited_neighbours(
        cell: Cell,
        grid: list[list[Cell]]
) -> list[tuple[Cell, DIRECTION]]:
    """
    Get the unvisited neighbours of a given cell in the grid.

    Args:
        cell (Cell): The cell for which to find neighbours.
        grid (list[list[Cell]]): The grid of cells.

    Returns:
        A list of tuples with the neighboring Cell objects and the direction
        in which the neighbour is.
    """
    x, y = cell.position
    neighbours: list[tuple[Cell, DIRECTION]] = []

    # Check the four cardinal directions
    if (y > 0 and not grid[y - 1][x].is_pattern
            and not grid[y - 1][x].visited):  # North
        neighbours.append((grid[y - 1][x], DIRECTION.NORTH))
    if (x < len(grid[0]) - 1 and not grid[y][x + 1].is_pattern
            and not grid[y][x + 1].visited):  # East
        neighbours.append((grid[y][x + 1], DIRECTION.EAST))
    if (y < len(grid) - 1 and not grid[y + 1][x].is_pattern
            and not grid[y + 1][x].visited):  # South
        neighbours.append((grid[y + 1][x], DIRECTION.SOUTH))
    if (x > 0 and not grid[y][x - 1].is_pattern
            and not grid[y][x - 1].visited):  # West
        neighbours.append((grid[y][x - 1], DIRECTION.WEST))

    return neighbours


def get_connected_neighbours(
        cell: Cell,
        grid: list[list[Cell]]
) -> list[tuple[Cell, DIRECTION]]:
    """
    Get the connected neighbours of a given cell in the grid. Connected meaning
    that the wall between both cells is not active.

    Args:
        cell (Cell): The cell for which to find neighbours.
        grid (list[list[Cell]]): The grid of cells.

    Returns:
        A list of neighboring Cell objects.
    """
    neighbours: list[tuple[Cell, DIRECTION]] = []

    x, y = cell.position

    if y > 0:
        north = grid[y - 1][x]

        if not (cell.walls & DIRECTION.NORTH.value):
            neighbours.append((north, DIRECTION.NORTH))

    if x < len(grid[0]) - 1:
        east = grid[y][x + 1]

        if not (cell.walls & DIRECTION.EAST.value):
            neighbours.append((east, DIRECTION.EAST))

    if y < len(grid) - 1:
        south = grid[y + 1][x]

        if not (cell.walls & DIRECTION.SOUTH.value):
            neighbours.append((south, DIRECTION.SOUTH))

    if x > 0:
        west = grid[y][x - 1]

        if not (cell.walls & DIRECTION.WEST.value):
            neighbours.append((west, DIRECTION.WEST))

    return neighbours


def get_not_connected_neighbours(
        cell: Cell,
        grid: list[list[Cell]]
) -> list[tuple[Cell, DIRECTION]]:
    """
    Get the unconnected neighbours of a given cell in the grid.
    Connected meaning that the wall between both cells is not active.

    Args:
        cell (Cell): The cell for which to find neighbours.
        grid (list[list[Cell]]): The grid of cells.

    Returns:
        A list of neighboring Cell objects.
    """
    neighbours: list[tuple[Cell, DIRECTION]] = []

    x, y = cell.position
    if y > 0:
        north = grid[y - 1][x]
        if cell.walls & DIRECTION.NORTH.value:
            neighbours.append((north, DIRECTION.NORTH))

    if x < len(grid[0]) - 1:
        east = grid[y][x + 1]
        if cell.walls & DIRECTION.EAST.value:
            neighbours.append((east, DIRECTION.EAST))

    if y < len(grid) - 1:
        south = grid[y + 1][x]
        if cell.walls & DIRECTION.SOUTH.value:
            neighbours.append((south, DIRECTION.SOUTH))

    if x > 0:
        west = grid[y][x - 1]
        if cell.walls & DIRECTION.WEST.value:
            neighbours.append((west, DIRECTION.WEST))

    return neighbours


def get_free_cells(grid: list[list[Cell]]) -> int:
    """
    Function that counts how many cells in the grid are not part of
    the '42' pattern.

    Args:
        mazegen (MazeGenerator): MazeGenerator object that stores the
        relevant information of the maze.
    Returns:
        An integer that represents the number of cells that are not part
        of the '42' pattern.
    """
    count: int = 0
    for row in grid:
        for cell in row:
            if not cell.is_pattern:
                count += 1
    return count


def unvisit_all_cells(grid: list[list[Cell]]) -> None:
    """
    Loops inside the grid to unvisit all the cells inside.

    Arguments:
        grid (list[list[Cell]]): Represents a 2D list of Cells.
    """
    for row in grid:
        for cell in row:
            if not cell.is_pattern:
                cell.visited = False


def active_solution_path(solution: list[Cell]) -> None:
    """
    Loops inside the list of cells changing the in_solution bool.

    Args:
        solution (list[Cell]): A list of Cells that are part of the solution.
    """
    for cell in solution:
        cell.in_solution = True


def opposite(direction: DIRECTION) -> DIRECTION:
    """
    Get the opposite direction of a given direction.

    Args:
        direction (DIRECTION): The direction for which
        to find the opposite.

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
