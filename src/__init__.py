"""
Expose the Config model and Maze generator as part of the package public API.
"""
from .generator import MazeGenerator
from .errors import ParamsError, InvalidConfigError

__all__ = ["MazeGenerator", "ParamsError", "InvalidConfigError"]
