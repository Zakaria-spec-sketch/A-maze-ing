import sys
from config_parser import parse_config
from maze_generator import MazeGenerator
from pathfinder import find_shortest_path
from file_writer import write_maze_file

from interaction import get_key, clear
from renderer import draw_maze, current_theme, THEMES
import renderer





def block_cell_by_index(grid, index, width):
    """يسد cell واحد حسب index"""
    x = index % width
    y = index // width
    cell = grid[y][x]
    cell.passable = False
    cell.north = True
    cell.south = True
    cell.east = True
    cell.west = True

    directions = [
        (0, -1, "south"),
        (1, 0, "west"),
        (0, 1, "north"),
        (-1, 0, "east")
    ]
    for dx, dy, opposite in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < len(grid):
            neighbor = grid[ny][nx]
            setattr(neighbor, opposite, True)


def interactive_mode(generator, config):
    grid = generator.generate_maze()
    

    show_path = False
    path = None

    while True:
        clear()

        if show_path:
            path = find_shortest_path(grid, config["entry"], config["exit"])

        draw_maze(
            grid,
            path=path,
            entry=config["entry"],
            exit_=config["exit"],
            pattern_42=generator.pattern_42
        )

        print("\n[R] regenerate | [P] toggle path | [C] color | [Q] quit")

        key = get_key()

        if key.lower() == "r":
            generator = MazeGenerator(
                width=config["width"],
                height=config["height"],
                perfect=config["perfect"]
            )
            grid = generator.generate_maze()

        elif key.lower() == "p":
            show_path = not show_path

        elif key.lower() == "c":
            renderer.current_theme = (renderer.current_theme + 1) % len(renderer.THEMES)

        elif key.lower() == "q":
            break


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    config = parse_config(sys.argv[1])

    generator = MazeGenerator(
        config["width"],
        config["height"],
        perfect=config["perfect"]
    )

    grid = generator.generate_maze()

    path = find_shortest_path(
        grid,
        config["entry"],
        config["exit"]
    )

    write_maze_file(
        config["output"],
        grid,
        config["entry"],
        config["exit"],
        path
    )

    interactive_mode(generator, config)


if __name__ == "__main__":
    main()
