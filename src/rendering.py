from .generator import Cell
from .enums import COLOR
from mlx import Mlx
from typing import Any
import os


class View:
    def __init__(
            self,
            window_width: int,
            window_height: int,
            cell_size: int,
            h_margin: int,
            v_margin: int,
            wall_size: int,
            grid: list[list[Cell]],
            theme: dict[str, COLOR]
    ) -> None:
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = cell_size
        self.h_margin = h_margin
        self.v_margin = v_margin
        self.wall_size = wall_size
        self.grid = grid
        self.theme = theme

    def key_handler(self, keycode: int, mlx: Mlx, win_ptr: int | None) -> None:
        if keycode == 49:
            print("Option 1 selected\nRe-generated a new maze")
        elif keycode == 50:
            print("Option 2 selected\nShow / Hide the shortest path")
        elif keycode == 51:
            print("Option 3 selected\nRotate the wall colours")
        elif keycode == 52:
            print("Option 4 selected\nExit")
            mlx.mlx_mouse_hook(win_ptr, None, None)
            os._exit(0)

    def generate_view(self) -> None:
        image_data, size_line, mlx, ptr = self.initialize_image()
        self.draw_complete_grid(image_data, size_line)
        self.write_options(mlx, ptr)
        self.show_image(mlx, ptr)

    def draw_complete_grid(self, image_data: Any, size_line: int) -> None:
        for row in self.grid:
            for cell in row:
                for i in range(self.cell_size):
                    for j in range(self.cell_size):
                        self.decide_if_pixel_is_drawn(
                            row, cell, i, j, image_data, size_line)

    def decide_if_pixel_is_drawn(
        self,
        row: list[Cell],
        cell: Cell,
        i: int,
        j: int,
        image_data: Any,
        size_line: int
    ) -> None:
        wall_size = self.wall_size
        
        self.draw_pixel(row, cell, i, j,
                            image_data, size_line, self.theme["background"])
        if (cell.is_pattern):
            self.draw_pixel(row, cell, i, j,
                            image_data, size_line, self.theme["pattern"])

        # define maze borders
        top: bool = (self.grid.index(row) == 0 and i <= wall_size * 2)
        bottom: bool = (self.grid.index(row) == len(self.grid) - 1
                        and i >= self.cell_size - wall_size * 2)
        left: bool = (row.index(cell) == 0 and j <= wall_size * 2)
        right: bool = (row.index(cell) == len(row) - 1
                       and j >= self.cell_size - wall_size * 2)

        # if we are in a border double the wall's thickness
        if (top or bottom or left or right):
            if (self.wall_size == wall_size):
                self.wall_size *= 2

        # if we are in a cell corner, draw
        start: int = self.wall_size
        end: int = self.cell_size - start
        if (i < start and j < start):
            if (self.grid.index(row) > 0 and row.index(cell) > 0):
                left_top_cell: Cell = self.grid[
                    self.grid.index(row) - 1][row.index(cell) - 1]
                if ((cell.walls >> 0) & 1 or (cell.walls >> 3) & 1
                        or (left_top_cell.walls >> 1) & 1
                        or (left_top_cell.walls >> 2) & 1):
                    self.draw_pixel(row, cell, i, j,
                                    image_data, size_line, self.theme["walls"])
        elif (j >= end and i < start):
            if (self.grid.index(row) > 0 and row.index(cell) < len(row) - 1):
                right_top_cell: Cell = self.grid[
                    self.grid.index(row) - 1][row.index(cell) + 1]
                if ((cell.walls >> 0) & 1 or (cell.walls >> 1) & 1
                        or (right_top_cell.walls >> 2) & 1
                        or (right_top_cell.walls >> 3) & 1):
                    self.draw_pixel(row, cell, i, j,
                                    image_data, size_line, self.theme["walls"])
        elif (j < start and i >= end):
            if (row.index(cell) > 0
                    and self.grid.index(row) < len(self.grid) - 1):
                left_bottom_cell: Cell = self.grid[
                    self.grid.index(row) + 1][row.index(cell) - 1]
                if ((cell.walls >> 2) & 1 or (cell.walls >> 3) & 1
                        or (left_bottom_cell.walls >> 0) & 1
                        or (left_bottom_cell.walls >> 1) & 1):
                    self.draw_pixel(row, cell, i, j,
                                    image_data, size_line, self.theme["walls"])
        elif (i >= end and j >= end):
            if (self.grid.index(row) < len(self.grid) - 1
                    and row.index(cell) < len(row) - 1):
                rigth_bottom_cell: Cell = self.grid[
                    self.grid.index(row) + 1][row.index(cell) + 1]
                if ((cell.walls >> 2) & 1 or (cell.walls >> 1) & 1
                        or (rigth_bottom_cell.walls >> 0) & 1
                        or (rigth_bottom_cell.walls >> 3) & 1):
                    self.draw_pixel(row, cell, i, j,
                                    image_data, size_line, self.theme["walls"])

        # if we are in a cell wall and the wall is placed, draw
        # top wall
        if (i < self.wall_size and (cell.walls >> 0) & 1):
            self.draw_pixel(row, cell, i, j,
                            image_data, size_line, self.theme["walls"])
        # bottom wall
        if (i >= self.cell_size - self.wall_size and (cell.walls >> 2) & 1):
            self.draw_pixel(row, cell, i, j,
                            image_data, size_line, self.theme["walls"])
        # left wall
        if (j < self.wall_size and (cell.walls >> 3) & 1):
            self.draw_pixel(row, cell, i, j,
                            image_data, size_line, self.theme["walls"])
        # right wall
        if (j >= self.cell_size - self.wall_size and (cell.walls >> 1) & 1):
            self.draw_pixel(row, cell, i, j,
                            image_data, size_line, self.theme["walls"])
        # restart wall size if altered
        if (self.wall_size != wall_size):
            self.wall_size //= 2

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
        px = row.index(cell) * self.cell_size + j
        py = self.grid.index(row) * self.cell_size + i
        start = self.offset(px, py, size_line)
        image_data[start:start + 4] = bytes(color.value)

    def offset(self, x: int, y: int, size_line: int) -> int:
        return y * size_line + x * 4

    def initialize_image(self) -> tuple[Any, int, Mlx, tuple[int | None,
                                                             int | None,
                                                             int | None]]:
        mlx = Mlx()
        mlx_ptr = mlx.mlx_init()
        win_ptr = mlx.mlx_new_window(
            mlx_ptr,
            self.window_width,
            self.window_height,
            "A-Maze-ing")
        mlx.mlx_clear_window(mlx_ptr, win_ptr)
        img_ptr = mlx.mlx_new_image(mlx_ptr, 2000, 2000)
        data, _, size_line, _ = mlx.mlx_get_data_addr(img_ptr)
        ptr = (mlx_ptr, win_ptr, img_ptr)
        return data, size_line, mlx, ptr

    def write_options(self, mlx: Mlx, ptr: tuple[int | None, ...]) -> None:
        options: list[str] = [
            "=== A-Maze-ing ===",
            "1. Re-generate a new maze",
            "2. Show / Hide the shortest path",
            "3. Rotate the wall colours",
            "4. Quit",
        ]
        i: float = 5
        for opt in options:
            mlx.mlx_string_put(ptr[0],
                               ptr[1],
                               int(self.h_margin / 2),
                               self.window_height - (self.cell_size * i),
                               0xFFFFFFFF,
                               opt)
            i -= 1

    def show_image(self, mlx: Mlx,
                   ptr: tuple[int | None, int | None, int | None]) -> None:
        mlx.mlx_put_image_to_window(ptr[0], ptr[1], ptr[2],
                                    int(self.h_margin / 2),
                                    int(self.h_margin / 2))

        def on_key(keynum: int, _: Any) -> None:
            self.key_handler(keynum, mlx, ptr[1])
        stuff = [1, 2]
        mlx.mlx_key_hook(ptr[1], on_key, stuff)
        mlx.mlx_loop(ptr[0])
