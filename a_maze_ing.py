from src.generator import MazeGenerator
from src.errors import ParamsError, InvalidConfigError
from src.algorithms import generate_maze_ab
from src.rendering import View
from src.enums import COLOR
from src.export import export_maze
from src.themes import THEMES


def main() -> None:
    try:
        horizontal_margin: int = 100
        vertical_margin: int = 380
        cell_size: int = 50
        wall_size: int = 2
        base_theme: tuple[str, dict[str, COLOR]] = THEMES[0]

        mazegen: MazeGenerator = MazeGenerator()
        mazegen.use_seed = True
        mazegen.grid = generate_maze_ab(mazegen)
        view = View(mazegen.config.width * cell_size + horizontal_margin,
                    mazegen.config.height * cell_size + vertical_margin,
                    cell_size,
                    horizontal_margin,
                    vertical_margin,
                    wall_size,
                    mazegen.grid,
                    base_theme)
        export_maze(mazegen)
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
