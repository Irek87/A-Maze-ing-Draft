from Canvas import Canvas
from Cell import Cell
import random

def generate_maze(canvas: Canvas, start_cell: Cell, rng: random.Random) -> None:

    if not canvas or not start_cell:
        return
    
    stack = [start_cell]
    start_cell.is_visited = True

    while stack:
        cell = stack[-1]

        neighbours = canvas.get_neighbours(cell)
        unvisited = [neighbour for neighbour in neighbours if not neighbour.is_visited]
        if unvisited:
            neighbour = rng.choice(unvisited)
            canvas.remove_wall(cell, neighbour)
            neighbour.is_visited = True
            stack.append(neighbour)
        else:
            accessible_neighbours = set(canvas.get_accessible_neighbours(cell))
            # inaccessible_neighbours = list(set(neighbours) - set(canvas.get_accessible_neighbours(cell)))
            inaccessible_neighbours = [neighbour for neighbour in neighbours if neighbour not in accessible_neighbours and neighbour not in canvas.ft_cells]
            if inaccessible_neighbours:
                neighbour_behind_wall = rng.choice(inaccessible_neighbours)
                canvas.dead_ends.add((cell, neighbour_behind_wall))
            stack.pop()


# RecursionError
# def generate_maze(canvas: Canvas, cell: Cell) -> None:
    # cell.is_visited = True
    # neighbours = canvas.get_neighbours(cell)
    # unvisited = [neighbour for neighbour in neighbours if not neighbour.is_visited]
    # if not unvisited:
    #     inaccessible_neighbours = list(set(neighbours) - set(canvas.get_accessible_neighbours(cell)))
    #     inaccessible_neighbours = [neighbour for neighbour in inaccessible_neighbours if neighbour not in canvas.ft_cells]
    #     if inaccessible_neighbours:
    #         neighbour_behind_wall = random.choice(inaccessible_neighbours)
    #         while neighbour_behind_wall in canvas.ft_cells:
    #             neighbour_behind_wall = random.choice(inaccessible_neighbours)
    #         canvas.dead_ends.add((cell, neighbour_behind_wall))
    #         return
    # while not all(neighbour.is_visited for neighbour in neighbours):
    #     neighbour = random.choice(neighbours)
    #     while neighbour.is_visited:
    #         neighbour = random.choice(neighbours)
    #     canvas.remove_wall(cell, neighbour)
    #     generate_maze(canvas, neighbour)
