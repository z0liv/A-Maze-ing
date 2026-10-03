from random import Random
from ..cell import Cell
from .alg_utils import get_free_cells, get_neighbours, opposite


def genmaze_ab(
        grid: list[list[Cell]],
        entry: Cell,
        rnd: Random
) -> list[list[Cell]]:
    """
        Generate the maze using the Aldous-Broder algorithm.

        Returns:
            A list of lists of cells that represents the grid.
    """
    current_cell = entry
    visited_cells = 1
    total_cells = get_free_cells(grid)
    while visited_cells < total_cells:
        neighbours = get_neighbours(current_cell, grid)
        next_cell, direction = rnd.choice(neighbours)
        if not next_cell.visited:
            current_cell.walls &= ~direction.value
            next_cell.walls &= ~opposite(direction).value
            next_cell.visited = True
            visited_cells += 1
        current_cell = next_cell
    return grid
