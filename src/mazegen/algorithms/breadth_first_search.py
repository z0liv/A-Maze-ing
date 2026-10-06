from .. import Cell
from .alg_utils import get_connected_neighbours, unvisit_all_cells


def solve_maze_bfs(
        grid: list[list[Cell]], entry: Cell, exit: Cell
) -> list[Cell]:
    """
    Function to solve the maze using the breadth first search algoritm.

    Args:
        grid (list[list[Cell]]): Represents a 2D list of Cells.
        entry: Entry Cell of the maze.
        entry: Exit Cell of the maze.
    
    Returns:
        A list of Cells that represents the solution path of the maze.
    """

    frontier: list[Cell] = [entry]
    visited: set[Cell] = {entry}
    parent: dict[Cell, Cell] = {}

    unvisit_all_cells(grid)
    while frontier:
        selected_cell: Cell = frontier.pop(0)

        if selected_cell == exit:
            break

        neighbours = get_connected_neighbours(selected_cell, grid)

        for neighbour, _ in neighbours:
            if neighbour not in visited:
                visited.add(neighbour)
                parent[neighbour] = selected_cell
                frontier.append(neighbour)

    solution: list[Cell] = []
    current = exit

    while current != entry:
        solution.append(current)
        current = parent[current]
    solution.append(entry)
    solution.reverse()
    return solution
