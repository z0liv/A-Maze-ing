from ..enums import DIRECTION
from ..generator import MazeGenerator, Cell
from .alg_utils import get_neighbors
from queue import Queue

def solve_maze_bfs(mazegen: MazeGenerator) -> list[DIRECTION]:

    q: Queue[Cell] = Queue()
    q.put(mazegen.entry)
    visited: set[Cell] = set()
    path: list[DIRECTION] = []
    while not q.empty():
        current = q.get()
        if current == mazegen.exit:
            return path
        neighbors = get_neighbors(current, mazegen.grid)
        for neighbor in neighbors:
            if neighbor[0] in visited:
                continue
            path.append(neighbor[1])
            q.put(neighbor[0])
            visited.add(neighbor[0])
    return []