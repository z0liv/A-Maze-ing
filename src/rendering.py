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
            wall_size: int
    ) -> None:
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = cell_size
        self.wall_size = wall_size

    def offset(self, x: int, y: int, size_line: int) -> int:
        return y * size_line + x * 4

    def generate_cell(
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

    def generate_view(self, grid: list[list[Cell]]) -> None:
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
        for row in grid:
            for cell in row:
                self.generate_cell(
                    data,
                    grid.index(row),
                    row.index(cell),
                    size_line)
        mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, int(self.cell_size / 2), int(self.cell_size / 2))

        def on_key(keynum: int, mystuff: Any) -> None:
            print(f"Got key {keynum}, and got my stuff back:")
            if keynum == 65307:
                mlx.mlx_mouse_hook(win_ptr, None, None)
                os._exit(0)
                print(mystuff)
        stuff = [1, 2]
        mlx.mlx_key_hook(win_ptr, on_key, stuff)
        mlx.mlx_hook(win_ptr, 33, 0, lambda _: os._exit(0), None)
        mlx.mlx_loop(mlx_ptr)
