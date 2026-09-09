import sys
import os


class InvalidConfigError(Exception):
    def __init__(self, message: str = "[ERROR] Invalid configuration"):
        self.message = message


class ParamsError(Exception):
    def __init__(
        self,
        message: str = "[ERROR] Program should have the correct parameters"
    ) -> None:
        self.message = message


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
                content: str
                with open(args[1]) as config:
                    content = config.read()
                    print(content)
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
