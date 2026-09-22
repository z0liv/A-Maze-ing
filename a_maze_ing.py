from src.generator import MazeGenerator
from src.errors import ParamsError, InvalidConfigError
from src.algorithms import generate_maze_ab
from src.rendering import View


def main() -> None:
    try:
        maze_generator: MazeGenerator = MazeGenerator()
        if hasattr(maze_generator, "config"):
            print(maze_generator.config)
        generate_maze_ab(maze_generator)
        view = View(2000, 2000, 8000, 40, 2)
        view.generate_view(maze_generator.grid)
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
