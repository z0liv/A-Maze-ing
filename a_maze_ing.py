from src.generator import MazeGenerator
from src.errors import ParamsError, InvalidConfigError
from src.algorithms import generate_maze_ab
from src.rendering import View


def main() -> None:
    try:
        horizontal_margin: int = 100
        vertical_margin: int = 350
        cell_size: int = 50
        wall_size: int = 4

        mazegen: MazeGenerator = MazeGenerator()
        generate_maze_ab(mazegen)
        view = View(mazegen.config.width * cell_size + horizontal_margin,
                    mazegen.config.height * cell_size + vertical_margin,
                    cell_size,
                    horizontal_margin,
                    vertical_margin,
                    wall_size,
                    mazegen.grid)
        for row in mazegen.grid:
            print()
            for cell in row:
                print(hex(cell.walls).removeprefix("0x"), end="")
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
