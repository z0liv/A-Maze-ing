"""
Expose the algorithms
"""
from .aldous_broder import genmaze_ab
from .depth_first_search import genmaze_dfs
from .breadth_first_search import solve_maze_bfs

__all__ = ["genmaze_ab", "genmaze_dfs", "solve_maze_bfs"]
