from src.generator import MazeGenerator
from src.errors import ParamsError, InvalidConfigError
from src.algorithms import genmaze_ab, genmaze_dfs, solve_maze_bfs
from src.rendering import View
from src.export import export_maze
import random


def main() -> None:
    try:
        mazegen: MazeGenerator = MazeGenerator()
        rnd = random.Random()
        if mazegen.config.algorithm == "ab":
            mazegen.grid = genmaze_ab(mazegen, rnd)
        else:
            mazegen.grid = genmaze_dfs(mazegen, rnd)
        view = View(mazegen)
        export_maze(mazegen)
        sol_cells = solve_maze_bfs(mazegen)
        for cell in sol_cells:
            print(cell.position)
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
