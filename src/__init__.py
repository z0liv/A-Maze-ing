"""
Expose the Config model and Maze generator as part of the package public API.
"""
from .generator import MazeGenerator, Cell
from .errors import ParamsError, InvalidConfigError
from .rendering import View

__all__ = ["MazeGenerator",
           "Cell",
           "ParamsError",
           "InvalidConfigError",
           "View",
           ]
