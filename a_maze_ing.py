from src.mazegen import MazeGenerator
from src.mazegen.errors import ParamsError, InvalidConfigError
from src.rendering import View
from src.config import load_config_model


def main() -> None:
    try:
        cfg = load_config_model()
        mazegen: MazeGenerator = MazeGenerator(
            cfg.width, cfg.height, cfg.entry, cfg.exit,
            cfg.output_file, False, cfg.perfect, cfg.seed,
            cfg.algorithm
        )
        view = View(mazegen, cfg)
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
