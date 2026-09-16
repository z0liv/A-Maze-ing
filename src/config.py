from pydantic import BaseModel, Field, model_validator
from typing import Annotated


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
    width: int = Field(ge=0, le=80)
    height: int = Field(ge=0, le=80)
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
