import sys
import os
from typing import Any
from src.config import Config


class InvalidConfigError(Exception):
    def __init__(self, message: str = "[ERROR] Invalid configuration"):
        self.message = message


class ParamsError(Exception):
    def __init__(
        self,
        message: str = "[ERROR] Program should have the correct parameters"
    ) -> None:
        self.message = message

def load_config(filename: str) -> Config:
    data: dict[str, Any] = {}
    with open(filename, "r") as config_file:
        for line in config_file:
            line = line.strip()
            key, value = line.split("=", 1)
            if (key.lower() == "entry" or key.lower() == "exit"):
                value = (value.split(","))
            data[key.lower()] = value
    configmodel: Config = Config(**data)
    return configmodel

def main() -> None:
    if 'VIRTUAL_ENV' in os.environ:
        try:
            args = sys.argv
            if len(args) == 1:
                prefix = "[ERROR] Missing config file, "
                raise ParamsError(
                    prefix + f"expected 1 received {len(args) - 1}"
                    )
            elif len(args) > 2:
                prefix = "[ERROR] Too many params, "
                raise ParamsError(
                    prefix + f"expected 1 received {len(args) - 1}"
                    )
            else:
                model: Config = load_config(args[1])
                print(model)
            """
            Expects a function that detects invalid config
            such as: impossible maze, bad syntax.
            Must raise InvalidConfigError with a clear message
            """
        except InvalidConfigError as error:
            print(error)
        except ParamsError as error:
            print(error)
        except FileNotFoundError as error:
            print("[ERROR]", error)
    else:
        print("WARNING: You're in the global environment!")
        print("To run this project you must be in a virtual environment")
        print("run:\npython -m venv .venv")
        print("source .venv/bin/activate")


if __name__ == "__main__":
    main()
