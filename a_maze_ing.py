from src.mazegen import MazeGenerator
from src.mazegen.errors import ParamsError, InvalidConfigError
from src.rendering import View
from src.config import load_config_model


def main() -> None:
    try:
        cfg = load_config_model()
        use_seed = False
        if cfg.seed is not None:
            use_seed = True
        mazegen: MazeGenerator = MazeGenerator(
            cfg.width, cfg.height, cfg.entry, cfg.exit,
            cfg.output_file, use_seed, cfg.perfect, cfg.seed,
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
