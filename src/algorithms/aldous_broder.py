import random
from ..generator import MazeGenerator, Cell
from ..enums import DIRECTION


def get_neighbors(
        cell: Cell,
        grid: list[list[Cell]]
) -> list[tuple[Cell, DIRECTION]]:
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
    if y > 0 and not grid[y - 1][x].is_pattern:  # North
        neighbors.append((grid[y - 1][x], DIRECTION.NORTH))
    if x < len(grid[0]) - 1 and not grid[y][x + 1].is_pattern:  # East
        neighbors.append((grid[y][x + 1], DIRECTION.EAST))
    if y < len(grid) - 1 and not grid[y + 1][x].is_pattern:  # South
        neighbors.append((grid[y + 1][x], DIRECTION.SOUTH))
    if x > 0 and not grid[y][x - 1].is_pattern:  # West
        neighbors.append((grid[y][x - 1], DIRECTION.WEST))

    return neighbors


def get_free_cells(mazegen: MazeGenerator) -> int:
    count: int = 0
    for row in mazegen.grid:
        for cell in row:
            if not cell.is_pattern:
                count += 1
    return count


def generate_maze_ab(mazegen: MazeGenerator) -> None:
    """
        Generate the maze using the Aldous-Broder algorithm.

        Args:
            mazegen (MazeGenerator): The maze generator instance.
    """
    current_cell = mazegen.entry
    visited_cells = 1
    total_cells = get_free_cells(mazegen)

    while visited_cells < total_cells:
        neighbors = get_neighbors(current_cell, mazegen.grid)
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
