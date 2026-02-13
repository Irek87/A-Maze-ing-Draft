from Cell import Cell
from Direction import Direction


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
