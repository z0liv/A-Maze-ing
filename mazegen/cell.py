class Cell:
    """
    Class that represents each cell of the maze.

    Attributes:
        position (tuple[int, int]): Defines the location of the cell in a tuple
                                    of x, y coordinates.
        walls (int): A integer that determines which walls are present.
        visited (bool): A boolean that tells if
                        the cell has been visited by the algorithm.
        is_pattern (bool): A boolean that tells if the cell is part of the
                           '42' pattern.
        is_entry (bool): A boolean that tells if the cell
                         is the entry of the maze.
        is_exit (bool): A boolean that tells if the cell
                         is the exit of the maze.
        visited (bool): A boolean that tells if
                        the cell has been visited by the algorithms.
        in_solution (bool): A boolean that tells if
                                the cell is part of the solution of the maze.
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
