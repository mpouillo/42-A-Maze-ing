
def create_grid(width, height):
    # All walls closed: bits N=1, E=1, S=1, W=1 => 0b1111 == 0xF
    return [[0xF for _ in range(width)] for _ in range(height)]


def cell_to_hex(cell):
    return format(cell & 0xF, "X")


def write_maze(grid, filename):
    # Write cells row by row, one hexadecimal digit per cell
    with open(filename, "w") as f:
        for row in grid:
            f.write("".join(cell_to_hex(c) for c in row) + "\n")


if __name__ == "__main__":
    WIDTH, HEIGHT = 21, 21
    maze = create_grid(WIDTH, HEIGHT)
    out = "maze_output.txt"
    write_maze(maze, out)
    print(f"Wrote {WIDTH}x{HEIGHT} maze to {out}")