from .generator import MazeGenerator


def export_maze(mazegen: MazeGenerator) -> None:
    try:
        with open(mazegen.config.output_file, "w") as file:
            content = list_content(mazegen)
            for element in content:
                file.write(element)
    except PermissionError as e:
        print(e)


def list_content(mazegen: MazeGenerator) -> list[str]:
    content: list[str] = list()
    for row in mazegen.grid:
        for cell in row:
            content.append(hex(cell.walls).removeprefix("0x"))
        content.append("\n")

    content.append("\n")
    content.append(f"{mazegen.config.entry[0]},{mazegen.config.entry[1]}")
    content.append("\n")
    content.append(f"{mazegen.config.exit[0]},{mazegen.config.exit[1]}")
    content.append("\n")
    return content
