#!/usr/bin/env python3

from algo.generate_maze import generate_maze
from maze_display import display_maze

if __name__ == "__main__":
    filename = generate_maze()
    display_maze(filename)
