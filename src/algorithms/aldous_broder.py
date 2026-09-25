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
        if next_cell.is_pattern:
            next_cell.visited = True
            visited_cells += 1
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
