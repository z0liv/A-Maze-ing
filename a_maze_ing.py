from src.generator import MazeGenerator


def main() -> None:
    maze_generator: MazeGenerator = MazeGenerator()
    print(maze_generator.config)


if __name__ == "__main__":
    main()
