import random
from typing import List
from cell import Cell
from maze_utils import get_neighbors


class MazeGenerator:
    def __init__(self, width: int, height: int,  perfect: bool = True):
        self.width = width
        self.height = height
        # self.seed = seed
        self.perfect = perfect
        # random.seed(seed)

        self.grid: List[List[Cell]] = self.create_grid()

    def create_grid(self) -> List[List[Cell]]:
        return [[Cell(x, y) for x in range(self.width)] for y in range(self.height)]
    def init_42_pattern(self):
        self.pattern_42 = set()

        if self.width < 12 or self.height < 12:
            return

        cx, cy = self.width // 2, self.height // 2

        pattern = [
            "10010 111",
            "10010   1",
            "11111 111",
            "00010 1  ",
            "00010 111",
        ]

        start_x = cx - 5
        start_y = cy - 2

        for dy, row in enumerate(pattern):
            for dx, val in enumerate(row):
                if val == "1":
                    x = start_x + dx
                    y = start_y + dy
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.pattern_42.add((x, y))
                        self.grid[y][x].passable = False  # 🚨 مهم

    def generate_maze(self) -> List[List[Cell]]:
        self.init_42_pattern() 

        for row in self.grid:
            for cell in row:
                cell.visited = False
                cell.north = cell.south = cell.east = cell.west = True

        stack = []
        current = self.grid[0][0]
        current.visited = True
    
        while True:
            neighbors = get_neighbors(self.grid, current)

            if neighbors:
                nxt = random.choice(neighbors)
                current.remove_wall(nxt)
                stack.append(current)
                nxt.visited = True
                current = nxt
            elif stack:
                current = stack.pop()
            else:
                break

        if not self.perfect:
            self._add_loops()

        return self.grid

    def _add_loops(self) -> None:
        for _ in range((self.width * self.height) // 10):
            x = random.randint(0, self.width - 2)
            y = random.randint(0, self.height - 2)
            cell = self.grid[y][x]
            neighbor = self.grid[y][x + 1]
            cell.remove_wall(neighbor)

    def add_42_pattern(self) -> None:
        self.pattern_42 = set()

        if self.width < 12 or self.height < 12:
            return

        cx, cy = self.width // 2, self.height // 2

        pattern = [
            "10010 111",
            "10010   1",
            "11111 111",
            "00010 1  ",
            "00010 111",
        ]

        start_x = cx - 5
        start_y = cy - 2

        def in_bounds(x, y):
            return 0 <= x < self.width and 0 <= y < self.height

        # STEP 1: mark all 42 cells
        for dy, row in enumerate(pattern):
            for dx, val in enumerate(row):
                if val == "1":
                    x = start_x + dx
                    y = start_y + dy
                    if in_bounds(x, y):
                        self.pattern_42.add((x, y))

        # STEP 2: CLEAR the zone (remove walls)
        for (x, y) in self.pattern_42:
            cell = self.grid[y][x]
            cell.north = cell.south = cell.east = cell.west = False

        # STEP 3: CONNECT only neighbors in pattern
        for (x, y) in self.pattern_42:
            for dx, dy in [(1,0), (0,1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in self.pattern_42:
                    self.grid[y][x].remove_wall(self.grid[ny][nx])


    def validate_maze(self) -> bool:
        return True  # Could implement connectivity checks
