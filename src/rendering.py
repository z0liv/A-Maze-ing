from .generator import Cell, MazeGenerator
from .enums import COLOR
from .algorithms import genmaze_ab, genmaze_dfs
from .export import export_maze
from .themes import THEMES
from mlx import Mlx
from typing import Any
import random
import os


class View:
    """
    Initialize the maze view.

    Args:
        window_width: The width in pixels of the window that shows the rendered
                      maze.
        window_height: The height in pixels of the window that shows the
                       rendered maze.
        cell_size: The size in pixels of each cell of the maze.
        h_margin: The added horizontal distances between the maze and the
                  window borders.
        v_margin: The added vertical distances between the maze and the
                  window borders.
        wall_size: The size in pixels of the walls of the maze.
        grid: A data structure that stores the data of all the cells in the
              maze.
        theme: A dictionary that stores the colors to apply to each part of the
               maze.
    """

    image_data: Any
    size_line: int
    ptr: tuple[int | None, ...]  # [mlx, win, image]
    mlx: Mlx

    def __init__(
            self,
            window_width: int,
            window_height: int,
            cell_size: int,
            h_margin: int,
            v_margin: int,
            wall_size: int,
            theme: tuple[str, dict[str, COLOR]],
            mazegen: MazeGenerator
    ) -> None:
        """
        Initialize the view with the attributes defined previously.
        """
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = cell_size
        self.h_margin = h_margin
        self.v_margin = v_margin
        self.wall_size = wall_size
        self.theme = theme
        self.mazegen = mazegen

    def key_handler(self, keycode: int, ptr: tuple[int | None, ...]) -> None:
        """
        Handles the user interactions through specific keys
        """
        if keycode == 49 or keycode == 65436:
            self.redo_maze()
        elif keycode == 50 or keycode == 65433:
            print("Option 2 selected\nShow / Hide the shortest path")
        elif keycode == 51 or keycode == 65435:
            bg = self.theme[1]["background"]
            primary = self.theme[1]["walls"]
            self.theme[1]['background'] = primary
            self.theme[1]['walls'] = bg
            self.draw_and_show(
                self.image_data, self.size_line, self.mlx, self.ptr)
        elif keycode == 52 or keycode == 65430:
            if self.theme[0] == 'nostromo':
                self.theme = THEMES[1]
            elif self.theme[0] == 'nautilus':
                self.theme = THEMES[2]
            else:
                self.theme = THEMES[0]
            self.draw_and_show(
                self.image_data, self.size_line, self.mlx, self.ptr)
        elif keycode == 53 or keycode == 65437:
            print("Exit")
            self.mlx.mlx_loop_exit(ptr[0])

    def redo_maze(self) -> None:
        self.mazegen = MazeGenerator()
        rnd = random.Random()
        if self.mazegen.config.algorithm == "ab":
            self.grid = genmaze_ab(self.mazegen, rnd)
        else:
            self.grid = genmaze_dfs(self.mazegen, rnd)
        export_maze(self.mazegen)
        self.draw_and_show(
            self.image_data, self.size_line, self.mlx, self.ptr)

    def generate_view(self) -> None:
        """
        The main method of the class, initializes the window and the image,
        and draws the maze along with the user interaction options.
        """
        image_data, size_line, mlx, ptr = self.initialize_image()
        self.draw_and_show(image_data, size_line, mlx, ptr)

    def draw_and_show(
        self, image_data: Any, size_line: int, mlx: Mlx,
        ptr: tuple[int | None, ...]
    ) -> None:
        self.write_options(mlx, ptr)
        self.draw_complete_grid(image_data, size_line)
        self.show_image(mlx, ptr)

    def draw_complete_grid(self, image_data: Any, size_line: int) -> None:
        """
        For each pixel in each cell, calls a function that decides if the pixel
        needs to be drawn
        """
        for row in self.mazegen.grid:
            for cell in row:
                for i in range(self.cell_size):
                    for j in range(self.cell_size):
                        self.draw_all_pixels(
                            row, cell, i, j, image_data, size_line)

    def draw_all_pixels(
        self,
        row: list[Cell],
        cell: Cell,
        i: int,
        j: int,
        image_data: Any,
        size_line: int
    ) -> None:
        """
        First draws every pixel with the background color,
        then draws the cells that belong to the pattern with the proper color,
        then draws the walls with the specified color in the theme.
        """
        wall_size = self.wall_size
        self.draw_pixel(row, cell, i, j,
                        image_data, size_line, self.theme[1]["background"])
        if (cell.is_pattern):
            self.draw_pixel(row, cell, i, j,
                            image_data, size_line, self.theme[1]["pattern"])
        elif (cell.is_entry):
            self.draw_pixel(row, cell, i, j,
                            image_data, size_line, self.theme[1]["entry"])
        elif (cell.is_exit):
            self.draw_pixel(row, cell, i, j,
                            image_data, size_line, self.theme[1]["exit"])

        # define maze borders
        top: bool = (self.mazegen.grid.index(row) == 0 and i <= wall_size * 2)
        bottom: bool = (
            self.mazegen.grid.index(row) == len(self.mazegen.grid) - 1
            and i >= self.cell_size - wall_size * 2
        )
        left: bool = (row.index(cell) == 0 and j <= wall_size * 2)
        right: bool = (row.index(cell) == len(row) - 1
                       and j >= self.cell_size - wall_size * 2)

        # if we are in a border double the wall's thickness
        if (top or bottom or left or right):
            if (self.wall_size == wall_size):
                self.wall_size *= 2

        # if we are in a cell corner that has a wall close, draw
        if (self.check_corner(row, cell, i, j)):
            self.draw_pixel(row, cell, i, j, image_data, size_line,
                            self.theme[1]["walls"])

        # if we are in a cell wall and the wall is placed, draw
        if ((i < self.wall_size and (cell.walls >> 0) & 1)  # top wall
                or (i >= self.cell_size - self.wall_size
                    and (cell.walls >> 2) & 1)  # bottom wall
                or (j < self.wall_size and (cell.walls >> 3) & 1)  # left wall
                or (j >= self.cell_size - self.wall_size
                    and (cell.walls >> 1) & 1)):  # right wall
            self.draw_pixel(row, cell, i, j,
                            image_data, size_line, self.theme[1]["walls"])

        # restart wall size if altered
        if (self.wall_size != wall_size):
            self.wall_size //= 2

    def offset(self, x: int, y: int, size_line: int) -> int:
        """
        Calculates the position of the pixel according to the size of a pixel
        and the size of each line.
        """
        return y * size_line + x * 4

    def draw_pixel(
            self,
            row: list[Cell],
            cell: Cell,
            i: int,
            j: int,
            image_data: Any,
            size_line: int,
            color: COLOR
    ) -> None:
        """
        Calculates the pixel position and modifies the bytes of the image that
        belong to that position with a specified color.
        """
        px = row.index(cell) * self.cell_size + j
        py = self.mazegen.grid.index(row) * self.cell_size + i
        start = self.offset(px, py, size_line)
        image_data[start:start + 4] = bytes(color.value)

    def check_corner(
            self,
            row: list[Cell],
            cell: Cell,
            i: int,
            j: int
    ) -> bool:
        """
        Cheks if the given position is part of a cell corner that needs
        to be drawn.
        """
        start: int = self.wall_size
        end: int = self.cell_size - start
        if (i < start and j < start):
            if (self.mazegen.grid.index(row) > 0 and row.index(cell) > 0):
                left_top_cell: Cell = self.mazegen.grid[
                    self.mazegen.grid.index(row) - 1][row.index(cell) - 1]
                if ((cell.walls >> 0) & 1 or (cell.walls >> 3) & 1
                        or (left_top_cell.walls >> 1) & 1
                        or (left_top_cell.walls >> 2) & 1):
                    return True
        elif (j >= end and i < start):
            if (self.mazegen.grid.index(row) > 0
                    and row.index(cell) < len(row) - 1):
                right_top_cell: Cell = self.mazegen.grid[
                    self.mazegen.grid.index(row) - 1][row.index(cell) + 1]
                if ((cell.walls >> 0) & 1 or (cell.walls >> 1) & 1
                        or (right_top_cell.walls >> 2) & 1
                        or (right_top_cell.walls >> 3) & 1):
                    return True
        elif (j < start and i >= end):
            if (row.index(cell) > 0
                and self.mazegen.grid.index(row) < len(
                    self.mazegen.grid) - 1):
                left_bottom_cell: Cell = self.mazegen.grid[
                    self.mazegen.grid.index(row) + 1][row.index(cell) - 1]
                if ((cell.walls >> 2) & 1 or (cell.walls >> 3) & 1
                        or (left_bottom_cell.walls >> 0) & 1
                        or (left_bottom_cell.walls >> 1) & 1):
                    return True
        elif (i >= end and j >= end):
            if (self.mazegen.grid.index(row) < len(self.mazegen.grid) - 1
                    and row.index(cell) < len(row) - 1):
                right_bottom_cell: Cell = self.mazegen.grid[
                    self.mazegen.grid.index(row) + 1][row.index(cell) + 1]
                if ((cell.walls >> 2) & 1 or (cell.walls >> 1) & 1
                        or (right_bottom_cell.walls >> 0) & 1
                        or (right_bottom_cell.walls >> 3) & 1):
                    return True
        return False

    def initialize_image(self) -> tuple[
        Any, int, Mlx, tuple[int | None, ...]
    ]:
        """
        Initializes the graphics, the window and the image with its data.
        """
        self.mlx = Mlx()
        mlx_ptr = self.mlx.mlx_init()
        win_ptr = self.mlx.mlx_new_window(
            mlx_ptr,
            self.window_width,
            self.window_height,
            "A-Maze-ing")
        self.mlx.mlx_clear_window(mlx_ptr, win_ptr)
        img_ptr = self.mlx.mlx_new_image(mlx_ptr, 2000, 2000)
        self.image_data, _, self.size_line, _ = self.mlx.mlx_get_data_addr(
            img_ptr)
        self.ptr = (mlx_ptr, win_ptr, img_ptr)
        return self.image_data, self.size_line, self.mlx, self.ptr

    def write_options(self, mlx: Mlx, ptr: tuple[int | None, ...]) -> None:
        """
        Function that writes the user interaction texts into the window.
        """
        options: list[str] = [
            "1. Re-generate a new maze",
            "2. Show / Hide the shortest path",
            "3. Rotate the wall colours",
            "4. Switch theme",
            "5. Exit",
        ]
        i = 5
        for opt in options:
            mlx.mlx_string_put(ptr[0],
                               ptr[1],
                               int(self.h_margin / 2),
                               self.window_height - (self.cell_size * i),
                               0xFFFFFFFF,
                               opt)
            i -= 1

    def show_image(self, mlx: Mlx, ptr: tuple[int | None, ...]) -> None:
        """
        Set the image in the window and add the key handler to it.
        """
        mlx.mlx_put_image_to_window(ptr[0], ptr[1], ptr[2],
                                    int(self.h_margin / 2),
                                    int(self.h_margin / 2))

        def on_key(keynum: int, _: Any) -> None:
            self.key_handler(keynum, ptr)

        def on_destroy(_: Any) -> None:
            mlx.mlx_loop_exit(ptr[0])
        stuff = [1, 2]
        mlx.mlx_key_hook(ptr[1], on_key, stuff)
        mlx.mlx_hook(ptr[1], 33, 0, on_destroy, None)
        mlx.mlx_loop(ptr[0])
        os._exit(0)
