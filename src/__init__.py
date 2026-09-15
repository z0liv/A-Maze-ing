"""Expose the Config model and Maze generator as part of the package public API."""
from .config import Config
from .generator import MazeGenerator

__all__ = ["Config", "MazeGenerator"]
