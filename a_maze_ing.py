import random
# import dfs
# from collections import deque
# from renderer import Renderer
# from Cell import Cell
# from Direction import Direction
from MazeGenerator import MazeGenerator

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


# def print_canvas(canvas: Canvas) -> None:
#     for y in range(canvas.height):
#         for x in range(canvas.width):
#             cell = canvas.get_cell(x, y)
#             print(f"{cell.direction.get_unicode()}", end=" ")
#         print()
#     print()
#     print(*canvas.entry, sep=", ")
#     print(*canvas.exit, sep=", ")


# def print_canvas_visits(canvas: Canvas) -> None:
#     print()
#     for y in range(canvas.height):
#         for x in range(canvas.width):
#             cell = canvas.get_cell(x, y)
#             print("0" if cell.is_visited else "-", end=" ")
#         print()

from Canvas import Canvas
def print_canvas_values(canvas: Canvas) -> None:
    print("\033c", end="")
    for y in range(canvas.height):
        for x in range(canvas.width):
            cell = canvas.get_cell(x, y)
            print(f"{cell.direction.value:x}".upper(), end="")
        print()

# def print_dead_ends(canvas: Canvas) -> None:
#     for cell1, cell2 in canvas.dead_ends:
#         print(cell1.coordinate, cell2.coordinate, end=" ")
#         print()


if __name__ == "__main__":
    # import sys
    # sys.setrecursionlimit(6000)

    width = 10
    height = 10
    entry = (0, 0)
    exit = (4, 4)

    maze_generator = MazeGenerator(42)
    maze_generator.set_canvas(width, height, entry, exit)
    maze_generator.set_renderer()
    maze_generator.generate_maze() # perfect
    # maze_generator.generate_maze(False) # imperfect
    maze_generator.solve_maze()

    try:
        while True:
            print_canvas_values(maze_generator.canvas)
            # maze_generator.renderer.render_maze()
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