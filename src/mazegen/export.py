from .generator import MazeGenerator


def export_maze(mazegen: MazeGenerator) -> None:
    """
    Function that writes the maze information into the
    output file given by the mazegen.config.
    """
    try:
        with open(mazegen.config.output_file, "w") as file:
            content = list_content(mazegen)
            for element in content:
                file.write(element)
    except PermissionError as e:
        print(e)


def list_content(mazegen: MazeGenerator) -> list[str]:
    """
    Format the maze information into the correct output format
    given by the subject.

    Transform each cell into hexadecimal removing the prefix.
    Looping the grid row by row adding cell by cell in the
    list to return as a string.

    Parameters:
        mazegen (MazeGenerator): MazeGenerator object that stores the
        relevant information of the maze.

    Returns:
        A list of each cell.walls transformed into hexadecimal.
        formatted into the expected output format to use it in the
        'maze_analizer.py'

    """
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
