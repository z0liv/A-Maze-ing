from .cell import Cell


def export_maze(
        grid: list[list[Cell]], entry: Cell,
        exit: Cell, output_file: str, solution: list[Cell]
) -> None:
    """
    Function that writes the maze information into the
    output file.

    Args:
        grid (list[list[Cell]]): Represents a 2D list of Cells.
        entry (Cell): Entry Cell of the maze.
        exit (Cell): Exit Cell of the maze.
        output_file (str): The name of the output file.
        solution (list[Cell]): A list of Cells that are
                              part of the solution path.
    """
    try:
        with open(output_file, "w") as file:
            content = list_content(
                grid, entry.position,
                exit.position, solution
            )
            for element in content:
                file.write(element)
    except PermissionError as e:
        print(e)


def get_solution_directions(solution: list[Cell]) -> str:
    """
    Loops inside the solution list verifiying each Cell
    with the next one to store the direction in the result
    string.

    Args:
        solution (list[Cell]): A list of the cells that are part of the
                               solution.
    Returns:
        A stirng with the directions of the solution.
    """
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
        grid: list[list[Cell]], entry: tuple[int, int],
        exit: tuple[int, int], solution: list[Cell]
) -> list[str]:
    """
    Format the maze information into the correct output format
    given by the subject.

    Transform each cell into hexadecimal removing the prefix.
    Looping the grid row by row adding cell by cell in the
    list to return as a string.

    Args:
        mazegen (MazeGenerator): MazeGenerator object that stores the
        relevant information of the maze.

    Returns:
        A list of each cell.walls transformed into hexadecimal, the
        entry and exit positions and the solution path in a string 
        represented by the cardinal directions 'NESW'.
        formatted into the expected output format to use it in the
        'maze_analizer.py'

    """
    content: list[str] = list()
    for row in grid:
        for cell in row:
            content.append(hex(cell.walls).removeprefix("0x"))
        content.append("\n")

    content.append("\n")
    content.append(f"{entry[0]},{entry[1]}")
    content.append("\n")
    content.append(f"{exit[0]},{exit[1]}")
    content.append("\n")
    content.append(get_solution_directions(solution))
    content.append("\n")

    return content
