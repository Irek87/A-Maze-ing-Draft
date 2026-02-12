from Direction import Direction

class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.coordinate = (x, y)
        self.is_visited = False
        self.direction = Direction.CLOSED
