from .generator import Cell
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
            grid: list[list[Cell]]
    ) -> None:
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = cell_size
        self.h_margin = h_margin
        self.v_margin = v_margin
        self.wall_size = wall_size
        self.grid = grid

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
        wall_size = self.wall_size
        for row in self.grid:
            for cell in row:
                for i in range(self.cell_size):
                    for j in range(self.cell_size):
                        if ((self.grid.index(row) == 0 and i <= wall_size * 2)
                            or (self.grid.index(row) == len(self.grid) - 1
                                and i >= self.cell_size - wall_size * 2)
                            or (row.index(cell) == 0 and j <= wall_size * 2)
                            or (row.index(cell) == len(row) - 1
                                and j >= self.cell_size - wall_size * 2)):
                            if (self.wall_size == wall_size):
                                self.wall_size *= 2
                        if ((i <= self.wall_size and j <= self.wall_size)
                            or (i >= self.cell_size - self.wall_size and j <= self.wall_size)
                            or (i <= self.wall_size and j >= self.cell_size - self.wall_size)
                            or (i >= self.cell_size - self.wall_size and j >= self.cell_size - self.wall_size)):
                            self.draw_pixel(row, cell, i, j, image_data, size_line)
                        if (i <= self.wall_size and (cell.walls >> 0) & 1):
                            self.draw_pixel(row, cell, i, j, image_data, size_line)
                        if (i >= self.cell_size - self.wall_size and (cell.walls >> 2) & 1):
                            self.draw_pixel(row, cell, i, j, image_data, size_line)
                        if (j <= self.wall_size and (cell.walls >> 3) & 1):
                            self.draw_pixel(row, cell, i, j, image_data, size_line)
                        if (j >= self.cell_size - self.wall_size and (cell.walls >> 1) & 1):
                            self.draw_pixel(row, cell, i, j, image_data, size_line)
                        if (self.wall_size != wall_size):
                            self.wall_size = wall_size

    def draw_pixel(
            self,
            row: list[Cell],
            cell: Cell,
            i: int,
            j: int,
            image_data: Any,
            size_line: int
    ):
        py = self.grid.index(row) * self.cell_size + i
        px = row.index(cell) * self.cell_size + j
        start = self.offset(px, py, size_line)
        image_data[start:start + 4] = bytes([0xFF, 0xFF, 0xFF, 0xFF])

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
