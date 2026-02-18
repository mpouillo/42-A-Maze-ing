from random import randint, seed
import numpy as np
from dotenv import load_dotenv
import os

seed(42)


load_dotenv("config.txt")

HEIGHT: int = int(os.environ.get("HEIGHT"))
WIDTH: int = int(os.environ.get("WIDTH"))
ENTRY = tuple(int(n) for n in os.environ.get("ENTRY").strip().split(','))
EXIT = tuple(int(n) for n in os.environ.get("EXIT").strip().split(','))


def get_logo() -> str:
    f = open("algo/logo.txt", "r")
    logo = f.read()
    f.close()
    return logo


def create_logo(logo, visited) -> np.ndarray:

    logo_rows = list(logo.strip().split('\n'))
    center = len(visited) // 5
    for i in range(0, len(logo_rows)):
        for j in range(0, len(logo_rows[0])):
            if logo_rows[i][j] == '1':
                visited[i + center, j + center] = True
    return visited


def gen_maze() -> np.ndarray:
    maze: np.ndarray = np.full((HEIGHT, WIDTH), 15, dtype=np.uint8)
    visited: np.ndarray = np.zeros((HEIGHT, WIDTH), dtype=bool)

    #visited = create_logo(get_logo(), visited)

    visited[ENTRY] = True
    stack: list = [ENTRY]

    def as_neighboors(cell) -> list:
        row, col = cell
        neighboors = []
        if row > 0 and not visited[row - 1, col]:
            neighboors.append((row - 1, col))
        if row < HEIGHT - 1 and not visited[row + 1, col]:
            neighboors.append((row + 1, col))
        if col > 0 and not visited[row, col - 1]:
            neighboors.append((row, col - 1))
        if col < WIDTH - 1 and not visited[row, col + 1]:
            neighboors.append((row, col + 1))
        return neighboors

    while stack:
        curr_cell = stack.pop()

        if as_neighboors(curr_cell):
            stack.append(curr_cell)

            next_cell = as_neighboors(curr_cell)[
                randint(0, len(as_neighboors(curr_cell)) - 1)]
            visited[next_cell] = True
            stack.append(next_cell)
            if next_cell[0] < curr_cell[0]:
                maze[curr_cell] &= 0xFF & ~(1 << 0)
                maze[next_cell] &= 0xFF & ~(1 << 2)
            elif next_cell[0] > curr_cell[0]:
                maze[curr_cell] &= 0xFF & ~(1 << 2)
                maze[next_cell] &= 0xFF & ~(1 << 0)
            elif next_cell[1] < curr_cell[1]:
                maze[curr_cell] &= 0xFF & ~(1 << 3)
                maze[next_cell] &= 0xFF & ~(1 << 1)
            elif next_cell[1] > curr_cell[1]:
                maze[curr_cell] &= 0xFF & ~(1 << 1)
                maze[next_cell] &= 0xFF & ~(1 << 3)
    return maze


def resolve_maze(maze):

    def close_cell(maze, row, col):

        rows, cols = maze.shape
        if not maze[row, col] & (1 << 0):
            maze[row, col] |= (1 << 0)
            if row > 0:
                maze[row-1, col] |= (1 << 2)

        if not maze[row, col] & (1 << 1):
            maze[row, col] |= (1 << 1)
            if col < cols - 1:
                maze[row, col+1] |= (1 << 3)

        if not maze[row, col] & (1 << 2):
            maze[row, col] |= (1 << 2)
            if row < rows - 1:
                maze[row+1, col] |= (1 << 0)

        if not maze[row, col] & (1 << 3):
            maze[row, col] |= (1 << 3)
            if col > 0:
                maze[row, col-1] |= (1 << 1)

    def get_all_deadend():
        deadend = []

        for row in range(maze.shape[0]):
            for col in range(maze.shape[1]):
                if bin(maze[row, col]).count("1") == 3 and (row, col)\
                      not in (ENTRY, EXIT):
                    deadend.append((row, col))

        return deadend

    while True:
        deadend = get_all_deadend()
        if not deadend:
            break

        for row, col in deadend:
            close_cell(maze, row, col)

    return maze
