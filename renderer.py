from colorama import init
init()

THEMES = [
    {"wall": "\033[37m", "path": "\033[32m", "entry": "\033[34m", "exit": "\033[31m"},
    {"wall": "\033[36m", "path": "\033[33m", "entry": "\033[35m", "exit": "\033[31m"},
    {"wall": "\033[90m", "path": "\033[92m", "entry": "\033[94m", "exit": "\033[91m"},
]

RESET = "\033[0m"
current_theme = 0


def get_colors():
    return THEMES[current_theme]


def draw_maze(grid, path=None, entry=None, exit_=None, pattern_42=None, player=None):
    colors = get_colors()
    WALL = colors["wall"]
    ENTRY = colors["entry"]
    EXIT = colors["exit"]

    h, w = len(grid), len(grid[0])

    # 🌈 Gradient
    gradient = ["\033[92m", "\033[93m", "\033[91m"]

    path_positions = []
    path_set = set()

    if path and entry:
        x, y = entry
        path_positions.append((x, y))
        for move in path:
            if move == "N": y -= 1
            elif move == "S": y += 1
            elif move == "E": x += 1
            elif move == "W": x -= 1
            path_positions.append((x, y))
        path_set = set(path_positions)

    for y in range(h):
        top = ""
        middle = ""

        for x in range(w):
            cell = grid[y][x]

            # ───── TOP (NO COLOR HERE)
            top += "┼───" if cell.north else "┼   "

            # ───── LEFT WALL
            if cell.west:
                middle += "│"
            else:
                middle += " "

            # ───── CONTENT (ALWAYS 3 CHARS VISIBLE)
            if (x, y) == entry:
                middle += ENTRY + " 🐵" + RESET

            elif (x, y) == exit_:
                middle += EXIT + " 🍌" + RESET

            elif player and (x, y) == player:
                middle += "\033[96m" + " P " + RESET

            elif pattern_42 and (x, y) in pattern_42:
                middle += "\033[95m" + "▓▒▓" + RESET

            elif (x, y) in path_set and not (pattern_42 and (x, y) in pattern_42):
                idx = path_positions.index((x, y))
                color = gradient[idx % len(gradient)]
                middle += color + " • " + RESET

            else:
                middle += "   "

        # ✅ APPLY COLOR ONCE PER LINE
        print(WALL + top + "┼" + RESET)
        print(WALL + middle + "│" + RESET)

    print(WALL + "┼───" * w + "┼" + RESET)
