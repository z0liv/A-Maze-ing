import sys
import os


def main() -> None:
    if 'VIRTUAL_ENV' in os.environ:
        args = sys.argv
        if len(args) == 1 or len(args) > 2:
            return (print("error"))
        else:
            content: str
            with open(args[1]) as config:
                content = config.read()
                print(content)
    else:
        print("WARNING: You're in the global environment!")
        print("To run this project you must be in a virtual environment")
        print("run:\npython -m venv .venv")
        print("source .venv/bin/activate")


if __name__ == "__main__":
    main()
