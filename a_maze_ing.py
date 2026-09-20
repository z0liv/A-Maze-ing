from src.generator import MazeGenerator, generate_maze_ab
from src.errors import ParamsError, InvalidConfigError


def main() -> None:
    try:
        maze_generator: MazeGenerator = MazeGenerator()
        if hasattr(maze_generator, "config"):
            print(maze_generator.config)
        generate_maze_ab(maze_generator)
        for row in maze_generator.grid:
            for cell in row:
                print(cell.position, cell.walls, cell.visited)
    except Exception as error:
        if isinstance(error, ParamsError):
            print("[ERROR]", error)
        elif isinstance(error, InvalidConfigError):
            print("[ERROR]", error)
        else:
            print(error)


if __name__ == "__main__":
    main()
