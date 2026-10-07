from .mazegen import MazeGenerator, Cell
from .enums import COLOR
from .themes import THEMES
from .config import Config
from mlx import Mlx
from typing import Any
import time


class View:

    """
    This class represents the view of the proyect, which manages everything
    related to the drawing and event handling with mlx

    Attributes:
        horizontal_margin (int): An integer that stores, in pixels,
            the needed margin within the window on the x axis
        vertical_margin (int): An integer that stores, in pixels,
            the needed margin within the window on the y axis
        cell_size (int): An integer that stores the size of the cells in pixels
        wall_sise (int): An integer that stores the size of each maze wall in
            pixels
        size_line (int): An integer that stores the size of a line of pixels
        ptr (tuple[int | None, ...]): A tuple of mlx pointers
        mlx (Mlx): The mlx object
        theme (tuple[str, dict[str, COLOR]]) : A tuple that stores the name of
            the theme and a dict that stores maze part name as the key and the
            color of it as the value.
    """

    horizontal_margin: int = 100
    vertical_margin: int = 380
    cell_size: int = 50
    wall_size: int = 2
    image_data: Any
    size_line: int
    show_solution: bool = False
    animating: bool = False
    animation_index: int = 0
    animation_delay: float = 0.05
    last_animation_delay: float = 0.0
    ptr: tuple[int | None, ...]  # [mlx, win, image]
    mlx: Mlx
    theme: tuple[str, dict[str, COLOR]] = THEMES[0]

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

    def __init__(self, mazegen: MazeGenerator, config: Config) -> None:
        """
        Initialize the view with the attributes defined previously.
        """
        self.config = config
        self.mazegen = mazegen
        if self.mazegen.width >= 25:
            self.vertical_margin = self.horizontal_margin * 2
        self.window_width = (mazegen.width * self.cell_size
                             + self.horizontal_margin)
        self.window_height = (mazegen.height * self.cell_size
                              + self.vertical_margin)

    def key_handler(self, keycode: int) -> None:
        """
        Handles the user interactions through specific keys
        """
        if keycode == 49 or keycode == 65436:
            self.show_solution = False
            self.animating = False
            self.redo_maze()
        elif keycode == 50 or keycode == 65433:
            if self.show_solution:
                self.show_solution = False
                self.animating = False
                self.draw_and_show()
            elif self.animation_index == len(self.mazegen.solution) - 1:
                self.show_solution = False
                self.animating = False
                self.animation_index = 0
                self.draw_and_show()
            else:
                self.show_solution = True
                self.toggle_solution_animation()
        elif keycode == 51 or keycode == 65435:
            bg = self.theme[1]["background"]
            primary = self.theme[1]["walls"]
            self.theme[1]['background'] = primary
            self.theme[1]['walls'] = bg
            self.show_solution = False
            self.animating = False
            self.draw_and_show()
        elif keycode == 52 or keycode == 65430:
            self.show_solution = False
            self.animating = False
            if self.theme[0] == 'nostromo':
                self.theme = THEMES[1]
            elif self.theme[0] == 'nautilus':
                self.theme = THEMES[2]
            else:
                self.theme = THEMES[0]
            self.draw_and_show()
        elif keycode == 53 or keycode == 65437:
            print("Exit")
            self.clean_shutdown()

    def redo_maze(self) -> None:
        """
        Creates new maze generator and random objects and calls the algorithm,
        the export function and the function that draws and shows the maze
        """
        cfg = self.config
        self.mazegen = MazeGenerator(
            cfg.width, cfg.height, cfg.entry, cfg.exit,
            cfg.output_file, False, cfg.perfect, cfg.seed,
            cfg.algorithm
        )
        self.draw_and_show()

    def generate_view(self) -> None:
        """
        The main method of the class, initializes the window and the image,
        and draws the maze along with the user interaction options.
        """
        self.initialize_image()
        self.draw_complete_grid()
        self.write_options()
        self.show_image()
        self.setup_hooks()
        self.mlx.mlx_loop(self.ptr[0])

    def clean_shutdown(self) -> None:
        self.mlx.mlx_loop_exit(self.ptr[0])

    def toggle_solution_animation(self) -> None:
        """Start or stop the solution animation."""

        if self.animating:
            self.animating = False
            self.show_solution = False
            self.animation_index = 0
            self.last_animation_delay = 0.0
            self.draw_and_show()
            return

        self.animation_index = 0
        self.last_animation_delay = 0.0
        self.animating = True

        self.draw_complete_grid()
        self.show_image()

    def draw_solution_step(self, cell: Cell) -> None:
        """Draw one solution cell."""

        x, y = cell.position

        self.draw_rectangle(
            x * self.cell_size + 2,
            y * self.cell_size + 2,
            self.cell_size - 5,
            self.cell_size - 5,
            self.theme[1]["solution"]
        )

    def animation_loop(self, _: Any) -> None:
        if not self.animating or not self.show_solution:
            self.show_solution = False
            self.animating = False
            return

        now = time.time()

        if now - self.last_animation_delay < self.animation_delay:
            return

        self.last_animation_delay = now

        if self.animation_index >= len(self.mazegen.solution) - 1:
            self.animating = False
            return
        if self.animation_index == 0:
            self.animation_index += 1
        cell = self.mazegen.solution[self.animation_index]

        self.draw_solution_step(cell)

        self.animation_index += 1

        self.show_image()

    def draw_and_show(self) -> None:
        """
        Calls the fucntion that writes the user interaction options, then the
        one that draws the grid, finally the one that shows the image that
        contains all the prevoiusly drawn pixels.
        """
        self.write_options()
        self.draw_complete_grid()
        self.show_image()

    def draw_complete_grid(self) -> None:
        """
        For each pixel in each cell, calls a function that decides if the pixel
        needs to be drawn.
        """
        self.set_background()

        for y, row in enumerate(self.mazegen.grid):
            for x, cell in enumerate(row):
                self.draw_cell(x, y, cell)

    def draw_cell(self, x: int, y: int, cell: Cell) -> None:
        """
        Function to draw independent Cells.
        """
        self.draw_cell_content(x, y, cell)
        self.draw_cell_walls(x, y, cell)

    def set_background(self) -> None:
        """
        Fill the maze area with the background color.
        """
        width = self.mazegen.width * self.cell_size
        height = self.mazegen.height * self.cell_size
        color = bytes(self.theme[1]["background"].value)

        for y in range(height):
            for x in range(width):
                start = self.offset(x, y)
                self.image_data[start:start + 4] = color

    def draw_cell_content(self, x: int, y: int, cell: Cell) -> None:
        margin = self.wall_size

        px = x * self.cell_size + margin
        py = y * self.cell_size + margin

        size = self.cell_size - 2 * margin

        if cell.is_pattern:
            color = self.theme[1]["pattern"]
        elif cell.is_entry:
            color = self.theme[1]["entry"]
        elif cell.is_exit:
            color = self.theme[1]["exit"]
        else:
            return

        self.draw_rectangle(px, py, size, size, color)

    def draw_cell_walls(
        self,
        x: int,
        y: int,
        cell: Cell
    ) -> None:

        px = x * self.cell_size
        py = y * self.cell_size
        wall = self.wall_size
        color = self.theme[1]["walls"]

        # North
        if cell.walls & 1:
            self.draw_rectangle(
                px, py,
                self.cell_size, wall,
                color
            )

        # West
        if cell.walls & 8:
            self.draw_rectangle(
                px, py,
                wall, self.cell_size,
                color
            )

        # East only on the right border
        if x == self.mazegen.width - 1 and cell.walls & 2:
            self.draw_rectangle(
                px + self.cell_size - wall,
                py,
                wall,
                self.cell_size,
                color
            )

        # South only on the bottom border
        if y == self.mazegen.height - 1 and cell.walls & 4:
            self.draw_rectangle(
                px,
                py + self.cell_size - wall,
                self.cell_size,
                wall,
                color
            )

    def draw_rectangle(
            self, x: int, y: int,
            width: int, height: int, color: COLOR
    ) -> None:
        for py in range(y, y + height):
            start = self.offset(x, py)
            end = start + width * 4

            self.image_data[start:end] = bytes(color.value) * width

    def offset(self, x: int, y: int) -> int:
        """
        Calculates the position of the pixel according to the size of a pixel
        and the size of each line.
        """
        return y * self.size_line + x * 4

    def draw_pixel(
            self,
            x: int,
            y: int,
            i: int,
            j: int,
            color: COLOR
    ) -> None:
        """
        Calculates the pixel position and modifies the bytes of the image that
        belong to that position with a specified color.
        """
        px = x * self.cell_size + j
        py = y * self.cell_size + i
        start = self.offset(px, py)
        self.image_data[start:start + 4] = bytes(color.value)

    def initialize_image(self) -> None:
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

        maze_width = self.mazegen.width * self.cell_size
        maze_height = self.mazegen.height * self.cell_size

        img_ptr = self.mlx.mlx_new_image(mlx_ptr, maze_width, maze_height)
        self.image_data, _, self.size_line, _ = self.mlx.mlx_get_data_addr(
            img_ptr)

        self.ptr = (mlx_ptr, win_ptr, img_ptr)

    def write_options(self) -> None:
        """
        Function that writes the user interaction texts into the window.
        """
        options: list[str] | str
        if len(self.mazegen.grid[0]) > 6:
            if len(self.mazegen.grid[0]) >= 25:
                options = ("1. Re-generate a new maze"
                           + "   2. Show / Hide the shortest path"
                           + "   3. Rotate the wall colours"
                           + "   4. Switch theme"
                           + "   5. Exit")
            else:
                options = [
                    "1. Re-generate a new maze",
                    "2. Show / Hide the shortest path",
                    "3. Rotate the wall colours",
                    "4. Switch theme",
                    "5. Exit"]
        else:
            options = [
                "1. Regen",
                "2. Path",
                "3. Color",
                "4. Theme",
                "5. Exit",
            ]
        if isinstance(options, list):
            i = 5
            for opt in options:
                py = self.window_height - (self.cell_size * i)
                self.mlx.mlx_string_put(self.ptr[0],
                                        self.ptr[1],
                                        int(self.horizontal_margin / 2),
                                        py,
                                        0xFFFFFF,
                                        opt)
                i -= 1
        else:
            self.mlx.mlx_string_put(self.ptr[0],
                                    self.ptr[1],
                                    int(self.horizontal_margin / 2),
                                    self.window_height - self.cell_size * 2,
                                    0xFFFFFF,
                                    options)

    def setup_hooks(self) -> None:
        """Register MLX event handlers."""
        self.mlx.mlx_key_hook(self.ptr[1], self.on_key, None)
        self.mlx.mlx_hook(self.ptr[1], 33, 0, self.on_destroy, None)
        self.mlx.mlx_loop_hook(self.ptr[0], self.animation_loop, None)

    def on_key(self, keycode: int, _: Any) -> None:
        """Handle keyboard input."""
        self.key_handler(keycode)

    def on_destroy(self, _: Any) -> None:
        """Handle window close."""
        self.clean_shutdown()

    def show_image(self) -> None:
        """
        Set the image in the window and add the key handler to it.
        """
        margin = self.horizontal_margin // 2
        self.mlx.mlx_put_image_to_window(self.ptr[0], self.ptr[1], self.ptr[2],
                                         margin, margin)
