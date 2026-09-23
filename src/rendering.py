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
            wall_size: int,
            grid: list[list[Cell]]
    ) -> None:
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = cell_size
        self.wall_size = wall_size
        self.grid = grid

    def key_handler(self,keycode: int, mlx: Mlx, win_ptr: int | None) -> None:
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
        self.show_image(mlx, ptr)

    def draw_complete_grid(self, image_data: Any, size_line: int) -> None:
        for row in self.grid:
            for cell in row:
                self.draw_cell(
                    image_data,
                    self.grid.index(row),
                    row.index(cell),
                    size_line)

    def draw_cell(
            self,
            data: Any,
            x: int,
            y: int,
            size_line: int
    ) -> None:
        for i in range(self.cell_size):
            for j in range(self.cell_size):
                if (i < self.wall_size
                   or i >= self.cell_size - self.wall_size
                   or j < self.wall_size
                   or j >= self.cell_size - self.wall_size):
                    px = x * self.cell_size + i
                    py = y * self.cell_size + j
                    start = self.offset(px, py, size_line)
                    data[start:start + 4] = bytes([0xFF, 0xFF, 0xFF, 0xFF])

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

    def show_image(self, mlx: Mlx,
                   ptr: tuple[int | None, int | None, int | None]) -> None:
        mlx.mlx_put_image_to_window(ptr[0], ptr[1], ptr[2],
                                    int(self.cell_size / 2),
                                    int(self.cell_size / 2))

        def on_key(keynum: int, _: Any) -> None:
            self.key_handler(keynum, mlx, ptr[2])
        stuff = [1, 2]
        mlx.mlx_key_hook(ptr[1], on_key, stuff)
        # mlx.mlx_hook(ptr[1], 33, 0, lambda _: os._exit(0), None)
        mlx.mlx_loop(ptr[0])
