#!/usr/bin/env python3

from mlx import Mlx
import os
from dotenv import load_dotenv
import sys


def parse_maze(filename) -> list[list]:
    '''Parse file and return maze data as list of lists'''
    try:
        array = []
        with open(filename, 'r') as maze_file:
            for line in maze_file:
                if not line.strip():
                    break
                row = []
                for c in line.strip():
                    row.append(int(c, 16))
                array.append(row)
        return array
    except Exception as e:
        print(f"Error while parsing maze output file: {e}")
        sys.exit(0)


def display_maze(filename: str):
    # MLX setup
    m = Mlx()
    mlx_ptr = m.mlx_init()
    if not mlx_ptr:
        print("Failed to initialize MLX")
        return

    # Get config
    load_dotenv("config.txt")

    # Get maze data from file
    MAZE = parse_maze(filename)

    # Get maze dimensions from config
    try:
        maze_width = int(os.environ.get("WIDTH"))
        maze_height = int(os.environ.get("HEIGHT"))
    except ValueError:
        sys.exit(0)

    # Window dimensions
    win_width = 1980
    win_height = 1080

    # 0.95 is a magic number to leave space around
    # SCALE_F = min(win_width / maze_width, win_height / maze_height) * 0.95
    LINE_WEIGHT = 4
    NODE_SIZE = max(1, round(
        min(maze_height, maze_width) / len(next(iter(MAZE), []))
    ))

    win_ptr = m.mlx_new_window(mlx_ptr, win_width, win_height, "A-Maze-ing")
    canvas_ptr = m.mlx_new_image(mlx_ptr,
                                 maze_width + LINE_WEIGHT,
                                 maze_width + LINE_WEIGHT)
    data, bpp, size_line, endian = m.mlx_get_data_addr(canvas_ptr)

    def draw_to_canvas(x, y, color):
        offset = (y * size_line) + (x * (bpp // 8))
        data[offset] = color & 0xFF                 # Blue
        data[offset + 1] = (color >> 8) & 0xFF      # Green
        data[offset + 2] = (color >> 16) & 0xFF     # Red
        data[offset + 3] = (color >> 24) & 0xFF     # Alpha

    def draw_node(start_x: int, start_y: int, value: int, color: int) -> None:
        if (
            start_x + NODE_SIZE > maze_width
            or start_y + NODE_SIZE > maze_height
        ):
            return

        if value & 1:   # Top
            for x in range(NODE_SIZE):
                for y in range(LINE_WEIGHT):
                    draw_to_canvas(start_x + x, start_y + y, color)
        if value & 2:   # Right
            for x in range(NODE_SIZE - LINE_WEIGHT, NODE_SIZE):
                for y in range(NODE_SIZE):
                    draw_to_canvas(start_x + x, start_y + y, color)
        if value & 4:   # Bottom
            for x in range(NODE_SIZE):
                for y in range(NODE_SIZE - LINE_WEIGHT, NODE_SIZE):
                    draw_to_canvas(start_x + x, start_y + y, color)
        if value & 8:   # Left
            for x in range(LINE_WEIGHT):
                for y in range(NODE_SIZE):
                    draw_to_canvas(start_x + x, start_y + y, color)

    x, y, i = 0, 0, 0
    for row in MAZE:
        for value in row:
            i += 1
            draw_node(x, y, value, 0xFFFFFFFF)
            x += NODE_SIZE - LINE_WEIGHT
        y += NODE_SIZE - LINE_WEIGHT
        x = 0

    m.mlx_put_image_to_window(
        mlx_ptr, win_ptr, canvas_ptr,
        max(0, round((win_width - maze_width) / 2)),
        max(0, round((win_height - maze_height) / 2))
    )

    def key_press(keycode, param):
        if keycode == 65307:    # Linux escape keycode
            m.mlx_release(mlx_ptr)

    m.mlx_key_hook(win_ptr, key_press, None)

    m.mlx_loop(mlx_ptr)


if __name__ == "__main__":
    display_maze("output_maze.txt")
