#!/usr/bin/env python3

from .generator import Cell
from mlx import Mlx  # type: ignore[import-untyped]
import os

def offset(x: int, y: int, size_line: int) -> int:
    return y * size_line + x * 4

def generate_cell(data, start: int) -> None:
    data[start:start + 4] = bytes([0xFF, 0xFF, 0xFF, 0xFF])

def generate_view(grid: list[list[Cell]]) -> None:
    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    win_ptr = mlx.mlx_new_window(mlx_ptr, 2000, 2000, "window")
    mlx.mlx_clear_window(mlx_ptr, win_ptr)
    img_ptr = mlx.mlx_new_image(mlx_ptr, 2000, 2000)
    data, bpp, size_line, fmt = mlx.mlx_get_data_addr(img_ptr)
    for row in grid:
        for cell in row:
            start = offset(grid.index(row) * 40, row.index(cell) * 40, size_line)
            generate_cell(data, start)
    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)

    def on_key(keynum: int, mystuff: object):
        print(f"Got key {keynum}, and got my stuff back:")
        print(mystuff)
        if keynum == 65307:
            mlx.mlx_mouse_hook(win_ptr, None, None)
            os._exit(0)
    stuff = [1, 2]
    mlx.mlx_key_hook(win_ptr, on_key, stuff)
    mlx.mlx_hook(win_ptr, 33, 0, lambda _: os._exit(0), None)
    mlx.mlx_loop(mlx_ptr)
