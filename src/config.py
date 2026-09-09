from pydantic import BaseModel, Field, model_validator
from typing import Annotated

class Config(BaseModel):
    width: int = Field(ge=0, le=80)
    height: int = Field(ge=0, le=80)
    entry: tuple[Annotated[int, Field(ge=0, le=80)],
                 Annotated[int, Field(ge=0, le=80)]]
    exit: tuple[Annotated[int, Field(ge=0, le=80)],
                Annotated[int, Field(ge=0, le=80)]]
    output_file: str = Field(default="maze.txt", max_length=25)
    perfect: bool
    seed: float = Field(ge=0.0, le=1.0)

    @model_validator(mode='after')
    def config_validation_rules(self) -> "Config":
        if (self.entry[0] > self.width):
            raise ValueError("Entry out of bounds")
        if (self.entry[0] > self.height):
            raise ValueError("Entry out of bounds")
        if (self.exit[0] > self.width):
            raise ValueError("Exit out of bounds")
        if (self.exit[0] > self.height):
            raise ValueError("Exit out of bounds")
        return self