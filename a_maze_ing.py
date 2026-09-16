from src.generator import MazeGenerator
from src.errors import ParamsError, InvalidConfigError


def main() -> None:
    try:
        maze_generator: MazeGenerator = MazeGenerator()
        if hasattr(maze_generator, "config"):
            print(maze_generator.config)
    except Exception as error:
        if isinstance(error, AttributeError):
            print("[ERROR]", error)
        elif isinstance(error, ParamsError):
            print("[ERROR]", error)
        elif isinstance(error, InvalidConfigError):
            print("[ERROR]", error)
        else:
            print(error)

if __name__ == "__main__":
    main()
