class Cell:
    """
    Class that represents each cell of the maze.

    Attributes:
        position (tuple[int, int]): Defines the location of the cell in a tuple
                                    of x, y coordinates.
        walls: (int): A integer that determines which walls are present.
        visited: (bool): A boolean that tells if
                         the cell is part of the solution(s).
    """
    position: tuple[int, int]
    walls: int
    visited: bool
    is_pattern: bool
    is_entry: bool
    is_exit: bool
    in_solution: bool = False

    def __init__(
            self, position: tuple[int, int],
            walls: int, visited: bool,
            is_pattern: bool, is_entry: bool,
            is_exit: bool
    ) -> None:
        """
        Initialize the cell with the attributes defined previously.
        """
        self.position = position
        self.walls = walls
        self.visited = visited
        self.is_pattern = is_pattern
        self.is_entry = is_entry
        self.is_exit = is_exit
