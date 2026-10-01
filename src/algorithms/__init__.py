"""
Expose the algorithms
"""
from .aldous_broder import generate_maze_ab
from .depth_first_search import generate_maze_dfs
from .breadth_first_search import solve_maze_bfs

__all__ = ["generate_maze_ab", "generate_maze_dfs"]
