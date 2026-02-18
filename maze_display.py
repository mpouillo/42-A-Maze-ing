#!/usr/bin/env python3

from mlx import Mlx
import os
from dotenv import load_dotenv
import sys


def parse_maze(filename: str) -> dict:
    '''Parse file and return maze data as list of lists'''
    try:
        data = {}
        array = []
        with open(filename, 'r') as maze_file:
            for line in maze_file:
                if not line.strip():
                    break
                row = []
                for c in line.strip():
                    row.append(int(c, 16))
                array.append(row)
            data.update({"maze": array})
            data.update(
                {"entry": tuple(
                    int(c) for c in maze_file.readline().strip().split(",")
                )}
            )
            data.update(
                {"exit": tuple(
                    int(c) for c in maze_file.readline().strip().split(",")
                )}
            )
            data.update({"path": maze_file.readline().strip()})
        return data
    except Exception as e:
        sys.exit(f"Error while parsing maze output file: {e}")


def display_maze(filename: str) -> None:
    # MLX setup
    m = Mlx()
    mlx_ptr = m.mlx_init()
    if not mlx_ptr:
        print("Failed to initialize MLX")
        return

    # Get config
    load_dotenv("config.txt")

    # Get maze data from file
    maze_data = parse_maze(filename)

    ENTRY = maze_data.get("entry")
    EXIT = maze_data.get("exit")
    PATH = maze_data.get("path")

    # Get maze dimensions from config
    try:
        maze_width = int(os.environ.get("WIDTH"))
        maze_height = int(os.environ.get("HEIGHT"))
    except ValueError:
        sys.exit("Error while parsing config file")

    # Window dimensions
    win_width, win_height = 1920, 1080

    # # 0.95 is a magic number to leave space around
    # SCALE_F = min(win_width / maze_width, win_height / maze_height) * 0.95
    LINE_WEIGHT = 3
    NODE_SIZE = max(1, round(
        min(maze_height, maze_width)
        / len(next(iter(maze_data.get("maze")), []))
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

    def draw_node_outline(start_x: int,
                          start_y: int,
                          value: int,
                          color: int) -> None:
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

    def draw_node_full(start_x: int, start_y: int, color: int) -> None:
        if (
            start_x + NODE_SIZE > maze_width
            or start_y + NODE_SIZE > maze_height
        ):
            return

        for x in range(LINE_WEIGHT, NODE_SIZE - LINE_WEIGHT):
            for y in range(LINE_WEIGHT, NODE_SIZE - LINE_WEIGHT):
                draw_to_canvas(start_x + x, start_y + y, color)

    def draw_path(maze_data) -> None:
        BLUE = 0xFF0000FF

        x = ENTRY[1] * (NODE_SIZE - LINE_WEIGHT)
        y = ENTRY[0] * (NODE_SIZE - LINE_WEIGHT)

        for direction in PATH:
            print(x, y)
            draw_node_full(x, y, BLUE)
            match direction:
                case "N":
                    y -= LINE_WEIGHT
                    draw_node_full(x, y, BLUE)
                    y -= NODE_SIZE - 2 * LINE_WEIGHT
                case "E":
                    x -= LINE_WEIGHT
                    draw_node_full(x, y, BLUE)
                    x -= NODE_SIZE - 2 * LINE_WEIGHT
                case "S":
                    y += LINE_WEIGHT
                    draw_node_full(x, y, BLUE)
                    y += NODE_SIZE - 2 * LINE_WEIGHT
                case "W":
                    x += LINE_WEIGHT
                    draw_node_full(x, y, BLUE)
                    x += NODE_SIZE - 2 * LINE_WEIGHT

    def draw_maze(maze_data):
        x, y = 0, 0
        MAZE = maze_data.get("maze")
        for row in MAZE:
            for value in row:
                draw_node_outline(x, y, value, 0xFFFFFFFF)
                x += NODE_SIZE - LINE_WEIGHT
            y += NODE_SIZE - LINE_WEIGHT
            x = 0

    ###draw_path(maze_data)
    draw_node_full(ENTRY[1] * (NODE_SIZE - LINE_WEIGHT),    # Entry point
                   ENTRY[0] * (NODE_SIZE - LINE_WEIGHT),
                   0xFF00FF00)  # Green
    draw_node_full(EXIT[1] * (NODE_SIZE - LINE_WEIGHT),     # Exit point
                   EXIT[0] * (NODE_SIZE - LINE_WEIGHT),
                   0xFFFF0000)  # Red
    draw_maze(maze_data)

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
