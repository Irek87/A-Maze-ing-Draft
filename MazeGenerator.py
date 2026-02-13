from Direction import Direction
from Canvas import Canvas
from renderer import Renderer
from collections import deque
from Cell import Cell
import dfs
import random


class MazeGenerator():
    def __init__(self, seed: int | None = None) -> None:
        self.seed = seed
        self.rng = random.Random(seed)

    def set_canvas(self, width: int, height: int, entry: tuple[int, int], exit: tuple[int, int]) -> None:
        self.canvas = Canvas(width, height, entry, exit)
        # self.cells_42: list[Cell] = []
        if width >= 9 and height >= 7:
            self.put_forty_two()

    def set_renderer(self):
        self.renderer = Renderer(self.canvas.width, self.canvas.height, self.canvas.entry, self.canvas.exit, [], "")

    def generate_maze(self, perfect: bool = True) -> None:
        self.perfect = perfect
        try:
            dfs.generate_maze(self.canvas, self.canvas.cells[0], self.rng)
            if not perfect:
                self.remove_dend_walls()
            while self.has_forbidden_opened_block():
                dfs.generate_maze(self.canvas, self.canvas.cells[0], self.rng)
                if not perfect:
                    self.remove_dend_walls()

            for y in range(self.canvas.height):
                for x in range(self.canvas.width):
                    cell = self.canvas.get_cell(x, y)
                    self.renderer.cells.append(cell.direction.value)
        except AttributeError as e:
            print("Got error:", e)

    def regenerate_maze(self) -> None:
        self.rng = random.Random(self.seed)
        self.renderer.cells = []
        self.renderer.show_path = False
        self.set_canvas(self.canvas.width, self.canvas.height, self.canvas.entry, self.canvas.exit)
        self.generate_maze(self.perfect)

    def remove_dend_walls(self) -> None:
        if not len(self.canvas.dead_ends):
            return
        for _ in range(len(self.canvas.dead_ends)//3 + 1):
            cell, neighbour = self.canvas.dead_ends.pop()
            # print("removing dead end wall", cell.coordinate, neighbour.coordinate)
            self.canvas.remove_wall(cell, neighbour)


    def put_forty_two(self) -> None:
        x_mid = self.canvas.width // 2
        y_mid = self.canvas.height // 2
        cells_to_close = [
            self.canvas.get_cell(x_mid-3, y_mid-2),
            self.canvas.get_cell(x_mid-3, y_mid-1),
            self.canvas.get_cell(x_mid-3, y_mid),
            self.canvas.get_cell(x_mid-2, y_mid),
            self.canvas.get_cell(x_mid-1, y_mid),
            self.canvas.get_cell(x_mid-1, y_mid+1),
            self.canvas.get_cell(x_mid-1, y_mid+2),

            self.canvas.get_cell(x_mid+1, y_mid-2),
            self.canvas.get_cell(x_mid+2, y_mid-2),
            self.canvas.get_cell(x_mid+3, y_mid-2),
            self.canvas.get_cell(x_mid+3, y_mid-1),
            self.canvas.get_cell(x_mid+3, y_mid),
            self.canvas.get_cell(x_mid+2, y_mid),
            self.canvas.get_cell(x_mid+1, y_mid),
            self.canvas.get_cell(x_mid+1, y_mid+1),
            self.canvas.get_cell(x_mid+1, y_mid+2),
            self.canvas.get_cell(x_mid+2, y_mid+2),
            self.canvas.get_cell(x_mid+3, y_mid+2)
        ]
        for cell in [cell for cell in cells_to_close if cell]:
            # self.cells_42.append(cell)
            cell.is_visited = True
            self.canvas.ft_cells.append(cell)

    def solve_maze(self) -> None:
        for cell in self.canvas.cells:
            cell.is_visited = False
        entry = self.canvas.entry
        entry_cell = self.canvas.get_cell(entry[0], entry[1])
        if not entry_cell:
            return
        queue = deque([(entry_cell, [entry_cell])])

        while queue:
            cell, path = queue.popleft()

            if not cell or cell.is_visited:
                continue

            cell.is_visited = True

            if cell.coordinate == self.canvas.exit:
                self.renderer.solution = self.convert_path_to_str(path)
                return

            for neighbour in self.canvas.get_accessible_neighbours(cell):
                if not neighbour.is_visited:
                    queue.append((neighbour, path + [neighbour]))

    def has_forbidden_opened_block(self) -> bool:
        opened = {cell.coordinate for cell in self.canvas.cells if cell.direction.value == Direction.OPENED.value}
        for x, y in opened:
            block = {(x + dx, y + dy) for dx in range(3) for dy in range(3)}
            if block.issubset(opened):
                return True
        return False


    @staticmethod
    def convert_path_to_str(path: list[Cell]) -> str:
        directions: list[str] = []
        dir_map = {
            (0, -1): "N",
            (0,  1): "S",
            (-1, 0): "W",
            (1,  0): "E",
        }

        for cur_cell, nxt_cell in zip(path, path[1:]):
            dx = nxt_cell.coordinate[0] - cur_cell.coordinate[0]
            dy = nxt_cell.coordinate[1] - cur_cell.coordinate[1]
            directions.append(dir_map.get((dx, dy), ""))

        return "".join(directions)
