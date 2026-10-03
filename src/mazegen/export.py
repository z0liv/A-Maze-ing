from ..config import Config
from .cell import Cell


def export_maze(
        grid: list[list[Cell]], config: Config, solution: list[Cell]
) -> None:
    """
    Function that writes the maze information into the
    output file given by the mazegen.config.
    """
    try:
        with open(config.output_file, "w") as file:
            content = list_content(grid, config, solution)
            for element in content:
                file.write(element)
    except PermissionError as e:
        print(e)


def get_solution_directions(solution: list[Cell]) -> str:
    result: str = ""
    current = solution[0]
    for next in solution[1:]:
        if (next.position[1] < current.position[1]
                and next.position[0] == current.position[0]):
            result += "N"
        elif (next.position[1] > current.position[1]
              and next.position[0] == current.position[0]):
            result += "S"
        elif (next.position[0] < current.position[0]
              and next.position[1] == current.position[1]):
            result += "W"
        elif (next.position[0] > current.position[0]
              and next.position[1] == current.position[1]):
            result += "E"
        current = next
    return result


def list_content(
        grid: list[list[Cell]], config: Config, solution: list[Cell]
) -> list[str]:
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
    for row in grid:
        for cell in row:
            content.append(hex(cell.walls).removeprefix("0x"))
        content.append("\n")

    content.append("\n")
    content.append(f"{config.entry[0]},{config.entry[1]}")
    content.append("\n")
    content.append(f"{config.exit[0]},{config.exit[1]}")
    content.append("\n")
    content.append(get_solution_directions(solution))

    return content
