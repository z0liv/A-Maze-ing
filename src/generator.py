import sys
from .config import Config
from .errors import InvalidConfigError, ParamsError
from typing import Any
from pydantic import ValidationError


class Cell:
    """
    Class that represents each cell of the maze.

    Attributes:
        position (tuple[int, int]): Defines de location of the cell in a tuple of x, y coordinates.
        walls: (int): A integer that determines which walls are present.
        visited: (bool): A boolean that tells if the cell is part of the solution(s).
    """
    position: tuple[int, int]
    walls: int
    visited: bool

    def __init__(
            self, position: tuple[int, int],
            walls: int, visited: bool
    ) -> None:
        """
        Initialize the cell with the attributes defined previously.
        """
        self.position = position
        self.walls = walls
        self.visited = visited


class MazeGenerator:
    """
    Class that will generate the maze.

    Attributes:
        config (Config): It stores all the info gathered from the config file.
        entry: (Cell): Indicates which cell is the entrance of the maze.
        exit: (Cell): Indicates which cell is the exit of the maze.
    """
    config: Config
    entry: Cell
    exit: Cell

    def __init__(self) -> None:
        """
        Initialize the maze.

        We do the config file parsing here.
        """
        try:
            self.config = load_config_model()
            self.entry = Cell(self.config.entry, 15, True)
            self.exit = Cell(self.config.exit, 15, True)
        except InvalidConfigError as error:
            print("[ERROR]", error)


def validate_params() -> str:
    """
        Validate that there is the correct number of params.

        Returns:
            The filename extracted from the sys.argv.
        Raises:
            ParamsError: If the number of params is equal to 1 or
                is greater than 2.
    """
    try:
        args = sys.argv
        if len(args) == 1:
            prefix = "Missing config file"
            raise ParamsError(prefix + ", expected 'config.txt'")
        elif len(args) > 2:
            prefix = "Too many params, "
            raise ParamsError(
                prefix + f"expected 1 received {len(args) - 1}"
                )
        return args[1]
    except ParamsError as error:
        print("[ERROR]", error)
        raise
    except FileNotFoundError as error:
        print("[ERROR]", error)
        raise
    except ValueError as error:
        print("[ERROR]", error)
        raise


def load_config_model() -> Config:
    """
        Reads the configuration file and loads its values
        into the Config model.

        Raises:
            ValueError: If the syntax of the config file is not "key=value".
            InvalidConfigError: If the configuration fails model validation.
    """
    filename = validate_params()
    data: dict[str, Any] = {}
    with open(filename, "r") as config_file:
        for line in config_file:
            line = line.strip()
            if line[0] == "#":
                continue
            try:
                key, value = line.split("=", 1)
                if (key.lower() == "entry" or key.lower() == "exit"):
                    lst_value = (value.split(","))
                    data[key.lower()] = lst_value
                else:
                    data[key.lower()] = value
            except ValueError:
                prefix: str = "[ERROR] Config lines in 'config.txt'"
                raise ValueError(prefix + " must be 'key=value' syntax")
    try:
        config_model: Config = Config(**data)
        return config_model
    except ValidationError as val:
        errors: list[str] = []
        for error in val.errors():
            if len(error.get("loc")) != 0:
                errors.append(str(error.get("loc")[0]) + ": " + error.get("msg"))
            else:
                errors.append(error.get("msg"))
        raise InvalidConfigError(errors)
