from src.mazegen import MazeGenerator
from src.mazegen.errors import ParamsError, InvalidConfigError
from src.rendering import View


def main() -> None:
    try:
        mazegen: MazeGenerator = MazeGenerator(True)
        view = View(mazegen)
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
