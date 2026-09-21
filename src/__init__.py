"""
Expose the Config model and Maze generator as part of the package public API.
"""
from .generator import MazeGenerator, Cell
from .errors import ParamsError, InvalidConfigError
from .mlx_test import generate_view

__all__ = ["MazeGenerator", "ParamsError", "InvalidConfigError", "generate_view", "Cell"]
