from random import Random
from ..cell import Cell
from .alg_utils import get_unvisited_neighbours, opposite


def genmaze_dfs(
        grid: list[list[Cell]], entry: Cell, rnd: Random
) -> list[list[Cell]]:
    """
        Generate the maze using the Depth First Search algorithm.

        Args:
            mazegen (MazeGenerator): The maze generator instance.
        Returns:
            A list of lists of cells that represents the grid.
    """

    def recursive_dfs(current: Cell) -> None:
        current.visited = True
        while True:
            neighbours = get_unvisited_neighbours(current, grid)
            if len(neighbours) == 0:
                return
            next_cell, direction = rnd.choice(neighbours)
            current.walls &= ~direction.value
            next_cell.walls &= ~opposite(direction).value
            recursive_dfs(next_cell)

    recursive_dfs(entry)
    return grid
