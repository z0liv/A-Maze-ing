import sys


def main() -> None:
    args = sys.argv
    if len(args) == 1 or len(args) > 2:
        return (print("error"))
    else:
        content: str
        with open(args[1]) as config:
            content = config.read()
            print(content)
    print("Hello, World!")


if __name__ == "__main__":
    main()
