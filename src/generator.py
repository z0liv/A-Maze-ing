import sys
from .config import Config
from typing import Any
from pydantic import ValidationError


class Cell:
    position: tuple[int, int]
    walls: int
    in_solution: bool

    def __init__(
            self, position: tuple[int, int],
            walls: int, in_solution: bool
    ) -> None:
        self.position = position
        self.walls = walls
        self.in_solution = in_solution


class MazeGenerator:
    config: Config
    entry: Cell
    exit: Cell

    def __init__(self) -> None:
        self.config = load_config_model()
        self.entry = Cell((0, 0), 15, True)
        self.exit = Cell((self.config.height, self.config.width), 15, True)


class InvalidConfigError(Exception):
    """
    Exception raised when the configuration is invalid.
    """
    def __init__(self, messages: list[str]) -> None:
        """
            Initialize the exception with a list of error messages.

            Args:
                messages: List of one or more error messages.
        """
        prefix: str = "[ERROR] Invalid configuration: "
        super().__init__(prefix + "\n{}".format("\n".join(messages)))
        self.messages = messages


class ParamsError(Exception):
    """
    Exception raised when the parameters are invalid.
    """
    def __init__(
        self,
        message: str = "[ERROR] Program should have the correct parameters"
    ) -> None:
        """
            Initialize the exception with an error message.

            Args:
                message: Error message to raise. Defaults to the
                standard parameter error message.
        """
        super().__init__(message)
        self.message = message


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
    except InvalidConfigError as error:
        print("[ERROR]", error)
        raise
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
            errors.append(str(error.get("loc")[0]) + ": " + error.get("msg"))
        raise InvalidConfigError(errors)
