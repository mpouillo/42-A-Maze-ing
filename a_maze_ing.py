#!/usr/bin/env python3

from mlx import Mlx
import sys
import os
from dotenv import load_dotenv


def main():
    m = Mlx()
    mlx_ptr = m.mlx_init()
    if not mlx_ptr:
        print("Failed to initialize MLX")
        return

    load_dotenv("config.txt")

    win_width = int(os.environ.get("WIDTH"))
    win_height = int(os.environ.get("HEIGHT"))
    win_ptr = m.mlx_new_window(mlx_ptr, win_width, win_height, "Test")

    img_ptr, img_w, img_h = m.mlx_png_file_to_image(mlx_ptr, "/home/mpouillo/Downloads/yotsuba.png")
    m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)

    def key_press(keycode, param):
        print(f"Key {keycode} pressed")
        if keycode == 53 or keycode == 65307:
            m.mlx_destroy_window(mlx_ptr, win_ptr)
            m.mlx_loop_exit(mlx_ptr)

    m.mlx_key_hook(win_ptr, key_press, None)

    print("Loop started. Press ESC to exit.")
    m.mlx_loop(mlx_ptr)


if __name__ == "__main__":
    main()
