#!/usr/bin/env python3

from mlx import Mlx
import os
from dotenv import load_dotenv
import sys


def main():
    m = Mlx()
    mlx_ptr = m.mlx_init()
    if not mlx_ptr:
        print("Failed to initialize MLX")
        return

    load_dotenv("config.txt")

    try:
        maze_width = int(os.environ.get("WIDTH"))
        maze_height = int(os.environ.get("HEIGHT"))
    except ValueError:
        sys.exit(0)

    win_width = 1980
    win_height = 1080

    # 0.95 is a magic number to leave space around
    SCALE_F = min(win_width / maze_width, win_height / maze_height) * 0.95
    NODE_SIZE = 20
    LINE_WEIGHT = 1

    maze_height = round(maze_height * SCALE_F)
    maze_width = round(maze_width * SCALE_F)

    print(maze_height, maze_width)

    win_ptr = m.mlx_new_window(mlx_ptr, win_width, win_height, "A-Maze-ing")
    canvas_ptr = m.mlx_new_image(mlx_ptr, win_width, win_height)
    data, bpp, size_line, endian = m.mlx_get_data_addr(canvas_ptr)

    def draw_to_canvas(x, y, color):
        offset = (y * size_line) + (x * (bpp // 8))
        data[offset] = color & 0xFF
        data[offset + 1] = (color >> 8) & 0xFF
        data[offset + 2] = (color >> 16) & 0xFF
        data[offset + 3] = (color >> 24) & 0xFF

    def draw_node(start_pos: tuple[int, int], value: int, color: int) -> None:
        sz = max(3, round(NODE_SIZE * SCALE_F))
        w = max(1, round(LINE_WEIGHT * SCALE_F))
        s_x, s_y = start_pos
        if value & 1:
            for x in range(sz):
                for y in range(w):
                    draw_to_canvas(s_x + x, s_y + y, color)
        if value & 2:
            for x in range(sz - w, sz):
                for y in range(sz):
                    draw_to_canvas(s_x + x, s_y + y, color)
        if value & 4:
            for x in range(sz):
                for y in range(sz - w, sz):
                    draw_to_canvas(s_x + x, s_y + y, color)
        if value & 8:
            for x in range(w):
                for y in range(sz):
                    draw_to_canvas(s_x + x, s_y + y, color)

    for i in range(0, maze_width, round(NODE_SIZE * SCALE_F)):
        for j in range(0, maze_height, round(NODE_SIZE * SCALE_F)):
            draw_node((i, j), 0xF, 0xFFFFFFFF)

    img_ptr, sz_x, sz_y = m.mlx_png_file_to_image(mlx_ptr, "img/yotsuba.png")

    m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr,
                              round((win_width - sz_y) / 2),
                              round((win_height - sz_x) / 2))

    m.mlx_put_image_to_window(
        mlx_ptr, win_ptr, canvas_ptr,
        round((win_width - maze_width - NODE_SIZE) / 2),
        round((win_height - maze_height - NODE_SIZE) / 2)
    )

    def key_press(keycode, param):
        if keycode == 65307:    # Linux escape keycode
            m.mlx_release(mlx_ptr)

    m.mlx_key_hook(win_ptr, key_press, None)

    m.mlx_loop(mlx_ptr)


if __name__ == "__main__":
    main()
