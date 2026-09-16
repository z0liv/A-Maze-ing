from src.generator import MazeGenerator
from src.errors import InvalidConfigError


def main() -> None:
    try:
        maze_generator: MazeGenerator = MazeGenerator()
        print(maze_generator.config)
    except InvalidConfigError as inv:
        print(inv)
    except AttributeError as attr:
        print(attr)

if __name__ == "__main__":
    main()
