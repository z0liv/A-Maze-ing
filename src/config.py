import sys
from pydantic import (BaseModel,
                      ValidationError,
                      Field,
                      model_validator)
from typing import Annotated, Any
from .errors import InvalidConfigError, ParamsError


class Config(BaseModel):
    """
        Configuration model for the maze generator.

        Inherits from BaseModel to provide data validation through Pydantic.

        Attributes:
            width (int): Width of the maze.
            height (int): Height of the maze.
            entry (tuple[int, int]): Coordinates of the entry point.
            exit (tuple[int, int]): Coordinates of the exit point.
            output_file (str): Name of the output file for the generated maze.
            perfect (bool): Whether to generate a perfect or imperfect maze.
            seed (float): Seed used to generate a specific maze.
"""
    width: int = Field(ge=0, le=35)
    height: int = Field(ge=0, le=20)
    entry: tuple[Annotated[int, Field(ge=0, le=80)],
                 Annotated[int, Field(ge=0, le=80)]]
    exit: tuple[Annotated[int, Field(ge=0, le=80)],
                Annotated[int, Field(ge=0, le=80)]]
    output_file: str = Field(default="maze.txt", max_length=25)
    perfect: bool = True
    seed: float = Field(default=0.123, ge=0.0, le=1.0)

    @model_validator(mode='after')
    def config_validation_rules(self) -> "Config":
        """
        Validate the entry and exit coordinates against the maze dimensions.
        Check if the entry is the same cell as the exit.
        Check if the entry or the exit are in the border of the maze.
        """
        if (self.output_file == ""):
            self.output_file = "maze.txt"
            print("Output file cannot be empty, using default 'maze.txt'.")
        if (self.entry[0] > self.width):
            raise ValueError("Entry out of bounds.")
        if (self.entry[1] > self.height):
            raise ValueError("Entry out of bounds.")
        if (self.exit[0] > self.width):
            raise ValueError("Exit out of bounds.")
        if (self.exit[1] > self.height):
            raise ValueError("Exit out of bounds.")
        if (self.entry[0] == self.exit[0] and self.entry[1] == self.exit[1]):
            raise ValueError("Entry and exit cannot be the same cell.")
        if (self.entry[0] == 0 or self.entry[0] == self.width):
            raise ValueError("Entry cannot be at the border of the maze.")
        if (self.entry[1] == 0 or self.entry[1] == self.height):
            raise ValueError("Entry cannot be at the border of the maze.")
        if (self.exit[0] == 0 or self.exit[0] == self.width):
            raise ValueError("Exit cannot be at the border of the maze.")
        if (self.exit[1] == 0 or self.exit[1] == self.height):
            raise ValueError("Exit cannot be at the border of the maze.")
        return self


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
    except Exception:
        raise


def load_config_model() -> Config:
    """
        Reads the configuration file and loads its values
        into the Config model.

        Raises:
            ValueError: If the syntax of the config file is not "key=value".
            InvalidConfigError: If the configuration fails model validation.
    """
    try:
        filename = validate_params()
        data: dict[str, Any] = {}
        with open(filename, "r") as config_file:
            for line in config_file:
                line = line.strip()
                if len(line) > 0:
                    if line[0] == "#":
                        continue
                else:
                    continue
                try:
                    key, value = line.split("=", 1)
                    if (key.lower() == "entry" or key.lower() == "exit"):
                        lst_value = (value.split(","))
                        data[key.lower()] = lst_value
                    else:
                        data[key.lower()] = value
                except ValueError:
                    prefix: str = "[ERROR] The configuration file"
                    raise ValueError(prefix + " must have 'key=value' syntax")
        config_model: Config = Config(**data)
        return config_model
    except ValidationError as val:
        errors: list[str] = []
        for error in val.errors():
            if len(error.get("loc")) != 0 and error.get("type") == "missing":
                prefix = error.get("msg") + ": '"
                errors.append(prefix + str(error.get("loc")[0]).upper() + "'")
            elif len(error.get("loc")) != 0:
                prefix = "'" + str(error.get("loc")[0]).upper()
                errors.append(prefix + "' " + error.get("msg"))
            else:
                errors.append(error.get("msg"))
        raise InvalidConfigError(errors)
