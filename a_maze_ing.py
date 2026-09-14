import sys
from typing import Any
from pydantic import ValidationError
from src.config import Config


class InvalidConfigError(Exception):
    """
    Exception raised when the configuration is invalid.
    """
    def __init__(self, messages: list[str]) -> None:
        """
            Initialize the exception with a list of error messages.

            Args:
                messages (list[str]): List of one or multiple error messages.
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
                message (str): Message to raise with the exception,
                with a default value.
        """
        super().__init__(message)
        self.message = message


def load_config(filename: str) -> None:
    """
        Read the configuration file and load its values into the Config model.

        Args:
            filename (str): Name of the file to open and read.

        Raises:
            ValueError: If the syntax of the config file is not "key=value".
            InvalidConfigError: If the model attributes are incorrect.
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
