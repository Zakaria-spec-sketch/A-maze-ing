from typing import List
from cell import Cell


def encode_cell(cell: Cell) -> str:
    value = 0
    value |= cell.north << 0
    value |= cell.east << 1
    value |= cell.south << 2
    value |= cell.west << 3
    return format(value, "X")


def write_maze_file(path, grid, entry, exit_, solution):
    with open(path, "w") as f:
        for row in grid:
            f.write(" ".join(encode_cell(c) for c in row) + "\n")

        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_[0]},{exit_[1]}\n")
        f.write(solution + "\n")
