from .. import MazeGenerator, Cell
from .alg_utils import get_connected_neighbours, unvisit_all_cells


def solve_maze_bfs(mazegen: MazeGenerator) -> list[Cell]:

    entry = mazegen.entry
    exit = mazegen.exit

    frontier: list[Cell] = [entry]
    visited: set[Cell] = {entry}
    parent: dict[Cell, Cell] = {}

    unvisit_all_cells(mazegen)
    while frontier:
        selected_cell: Cell = frontier.pop(0)

        if selected_cell == exit:
            break

        neighbours = get_connected_neighbours(selected_cell, mazegen.grid)

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
