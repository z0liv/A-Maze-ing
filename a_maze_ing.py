import sys
from typing import Any
from pydantic import ValidationError
from src.config import Config


class InvalidConfigError(Exception):
    """
    Custom error class to catch invalid config errors.
    """
    def __init__(self, messages: list[str]) -> None:
        """
            Initialize the error message list.

            Attributes:
                messages (list[str]): List of one or multiple error messages.
        """
        prefix: str = "[ERROR] Invalid configuration: "
        super().__init__(prefix + "\n{}".format("\n".join(messages)))
        self.messages = messages


class ParamsError(Exception):
    """
    Custom error class to catch errors on parameters.
    """
    def __init__(
        self,
        message: str = "[ERROR] Program should have the correct parameters"
    ) -> None:
        """
            Initialize the error message.

            Attributes:
                message (str): Message to raise with the exception,
                with a default value.
        """
        super().__init__(message)
        self.message = message


def load_config(filename: str) -> None:
    """
        Reads the config file from the filename given by parameter,
        and stores it in the Config Model.

        Parameters:
            filename (str): Name of the file to open and read.

        Returns:
            None
    """
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
        configmodel: Config = Config(**data)
        print(configmodel)
    except ValidationError as val:
        errors: list[str] = []
        for error in val.errors():
            errors.append(str(error.get("loc")[0]) + ": " + error.get("msg"))
        raise InvalidConfigError(errors)


def main() -> None:
    """
        Main function that initializes the program.

        Returns:
            None
    """
    try:
        args = sys.argv
        if len(args) == 1:
            prefix = "[ERROR] Missing config file"
            raise ParamsError(prefix + ", expected 'config.txt'")
        elif len(args) > 2:
            prefix = "[ERROR] Too many params, "
            raise ParamsError(
                prefix + f"expected 1 received {len(args) - 1}"
                )
        else:
            load_config(args[1])
    except InvalidConfigError as error:
        print(error)
    except ParamsError as error:
        print(error)
    except FileNotFoundError as error:
        print("[ERROR]", error)
    except ValueError as error:
        print("[ERROR]", error)


if __name__ == "__main__":
    main()
