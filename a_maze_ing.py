from src.generator import MazeGenerator
from src.errors import ParamsError, InvalidConfigError
from src.algorithms import generate_maze_ab
from src.rendering import View


def main() -> None:
    try:
        margin: int = 150
        cell_size: int = 50
        wall_size: int = 4

        mazegen: MazeGenerator = MazeGenerator()
        generate_maze_ab(mazegen)
        view = View(mazegen.config.width * cell_size + margin,
                    mazegen.config.height * cell_size + margin,
                    cell_size,
                    margin,
                    wall_size,
                    mazegen.grid)
        view.generate_view()
    except Exception as error:
        if isinstance(error, ParamsError):
            print("[ERROR]", error)
        elif isinstance(error, InvalidConfigError):
            print("[ERROR]", error)
        else:
            print(error)


if __name__ == "__main__":
    main()
