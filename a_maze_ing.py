from mazegen import MazeGenerator
from mazegen import ParamsError, InvalidConfigError
from config import load_config_model
from rendering import View


def main() -> None:
    """
    Main function of the project.

    Reads the config file and stores the values on the
    Config instance and instances the MazeGenerator
    loads the instances into the View class and generates the view.
    """
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
    except ParamsError as error:
        print("[ERROR]", error)
    except InvalidConfigError as error:
        print("[ERROR]", error)
    except PermissionError as error:
        print(error)
    except FileNotFoundError as error:
        print(error)
    except KeyboardInterrupt as error:
        print(error)
    except OSError as error:
        print(error)
    except Exception as error:
        print(error)


if __name__ == "__main__":
    main()
