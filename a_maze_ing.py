import random
import dfs
from collections import deque
from renderer import Renderer
from Cell import Cell
from Direction import Direction

# Closed wall sets bit to 1, open - 0
# Binary  Hex  W  S  E  N
# 0000    0    O  O  O  O
# 0001    1    O  O  O  C
# 0010    2    O  O  C  O
# 0011    3    O  O  C  C
# 0100    4    O  C  O  O
# 0101    5    O  C  O  C
# 0110    6    O  C  C  O
# 0111    7    O  C  C  C
# 1000    8    C  O  O  O
# 1001    9    C  O  O  C
# 1010    A    C  O  C  O
# 1011    B    C  O  C  C
# 1100    C    C  C  O  O
# 1101    D    C  C  O  C
# 1110    E    C  C  C  O
# 1111    F    C  C  C  C




class Canvas():
    def __init__(self, width: int, height: int, entry: tuple[int, int], exit: tuple[int, int]) -> None:
        self.width: int = width
        self.height: int = height
        self.cells: list[Cell] = []
        self.ft_cells: list[Cell] = []
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.dead_ends: set[tuple[Cell, Cell]] = set()

        for x in range(width):
            for y in range(height):
                self.cells.append(Cell(x,y))

    def get_cell(self, x: int, y: int) -> Cell | None:
        for cell in self.cells:
            if cell.coordinate == (x, y):
                return cell
        return None

    def get_neighbours(self, cell: Cell) -> list[Cell]:
        neighbours: list[Cell | None] = []
        if cell:
            x = cell.coordinate[0]
            y = cell.coordinate[1]

            if x - 1 >= 0:
                neighbours.append(self.get_cell(x-1, y))
            if x + 1 < self.width:
                neighbours.append(self.get_cell(x+1, y))
            if y - 1 >= 0:
                neighbours.append(self.get_cell(x, y-1))
            if y + 1 < self.height:
                neighbours.append(self.get_cell(x, y+1))
        return [neighbour for neighbour in neighbours if neighbour]

    def get_accessible_neighbours(self, cell: Cell) -> list[Cell]:
        accessible_neighbours: list[Cell] = []
        x, y = cell.coordinate

        for neighbour in self.get_neighbours(cell):
            nx, ny = neighbour.coordinate

            # neighbour is NORTH of cell
            if ny == y - 1:
                if neighbour.direction.can_see(Direction.S) and cell.direction.can_see(Direction.N):
                    accessible_neighbours.append(neighbour)

            # neighbour is SOUTH of cell
            elif ny == y + 1:
                if neighbour.direction.can_see(Direction.N) and cell.direction.can_see(Direction.S):
                    accessible_neighbours.append(neighbour)

            # neighbour is WEST of cell
            elif nx == x - 1:
                if neighbour.direction.can_see(Direction.E) and cell.direction.can_see(Direction.W):
                    accessible_neighbours.append(neighbour)

            # neighbour is EAST of cell
            elif nx == x + 1:
                if neighbour.direction.can_see(Direction.W) and cell.direction.can_see(Direction.E):
                    accessible_neighbours.append(neighbour)
        return accessible_neighbours

    def remove_wall(self, cell: Cell, neighbour: Cell) -> None:
        if neighbour in self.ft_cells:
            return

        x, y = cell.coordinate[0], cell.coordinate[1]

        # neighbour is WEST of cell
        if neighbour.coordinate == (x-1, y):
            cell.direction = Direction(cell.direction.value - 8)
            neighbour.direction = Direction(neighbour.direction.value - 2)
        # neighbour is NORTH of cell
        elif neighbour.coordinate == (x, y-1):
            cell.direction = Direction(cell.direction.value - 1)
            neighbour.direction = Direction(neighbour.direction.value - 4)
        # neighbour is EAST of cell
        elif neighbour.coordinate == (x+1, y):
            cell.direction = Direction(cell.direction.value - 2)
            neighbour.direction = Direction(neighbour.direction.value - 8)
        # neighbour is SOUTH of cell
        elif neighbour.coordinate == (x, y+1):
            cell.direction = Direction(cell.direction.value - 4)
            neighbour.direction = Direction(neighbour.direction.value - 1)


class MazeGenerator():

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
            dfs.generate_maze(self.canvas, self.canvas.cells[0])
            if not perfect:
                self.remove_dend_walls()
            while self.has_forbidden_opened_block():
                dfs.generate_maze(self.canvas, self.canvas.cells[0])
                if not perfect:
                    self.remove_dend_walls()

            for y in range(self.canvas.height):
                for x in range(self.canvas.width):
                    cell = self.canvas.get_cell(x, y)
                    self.renderer.cells.append(cell.direction.value)
        except AttributeError as e:
            print("Got error:", e)

    def regenerate_maze(self) -> None:
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


def print_canvas(canvas: Canvas) -> None:
    for y in range(canvas.height):
        for x in range(canvas.width):
            cell = canvas.get_cell(x, y)
            print(f"{cell.direction.get_unicode()}", end=" ")
        print()
    print()
    print(*canvas.entry, sep=", ")
    print(*canvas.exit, sep=", ")


def print_canvas_visits(canvas: Canvas) -> None:
    print()
    for y in range(canvas.height):
        for x in range(canvas.width):
            cell = canvas.get_cell(x, y)
            print("0" if cell.is_visited else "-", end=" ")
        print()


def print_canvas_values(canvas: Canvas) -> None:
    for y in range(canvas.height):
        for x in range(canvas.width):
            cell = canvas.get_cell(x, y)
            print(f"{cell.direction.value:x}".upper(), end=" ")
        # print()

def print_dead_ends(canvas: Canvas) -> None:
    for cell1, cell2 in canvas.dead_ends:
        print(cell1.coordinate, cell2.coordinate, end=" ")
        print()


if __name__ == "__main__":
    width = 5
    height = 5
    entry = (0, 0)
    exit = (4, 4)

    random.seed(42)

    maze_generator = MazeGenerator()
    maze_generator.set_canvas(width, height, entry, exit)
    maze_generator.set_renderer()
    maze_generator.generate_maze() # perfect
    # maze_generator.generate_maze(False) # imperfect
    maze_generator.solve_maze()

    try:
        while True:
            maze_generator.renderer.render_maze()
            # render_maze(WALL_COLORS[color_index], show_path)
            print("\n=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")
            choice = input("Choice? (1-4): ")

            if choice == "1":
                maze_generator.regenerate_maze() # perfect
                # maze_generator.regenerate_maze(False) # imperfect
                maze_generator.solve_maze()
            elif choice == "2":
                maze_generator.renderer.show_path = not maze_generator.renderer.show_path
            elif choice == "3":
                maze_generator.renderer.color_index = (maze_generator.renderer.color_index + 1) % len(maze_generator.renderer.wall_colors)
            elif choice == "4":
                print("Bye!")
                break
    except KeyboardInterrupt:
        print("\nBye!")