import random
from ..generator import MazeGenerator, Cell
from .alg_utils import get_free_cells, get_neighbors, opposite


def generate_maze_ab(mazegen: MazeGenerator,
                     rnd: random.Random) -> list[list[Cell]]:
    """
        Generate the maze using the Aldous-Broder algorithm.

        Args:
            mazegen (MazeGenerator): The maze generator instance.
        Returns:
            A list of lists of cells that represents the grid.
    """
    current_cell = mazegen.entry
    visited_cells = 1
    total_cells = get_free_cells(mazegen)
    while visited_cells < total_cells:
        neighbors = get_neighbors(current_cell, mazegen.grid)
        next_cell, direction = rnd.choice(neighbors)
        if not next_cell.visited:
            current_cell.walls &= ~direction.value
            next_cell.walls &= ~opposite(direction).value
            next_cell.visited = True
            visited_cells += 1
        current_cell = next_cell
    return mazegen.grid
