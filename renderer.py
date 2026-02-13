"""Terminal maze renderer using block characters."""

import time
# from Cell import Cell
from enum import Enum


# PRESETS
class Presets(Enum):
    WALL = "██"
    PATH = "  "
    RESET = "\033[0m"
    GREY = "\033[90m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"


class Renderer():
    # HELPERS:
    walls = [
        (1, -1,  0, -1, +1),  # North: wall above + corner above-right
        (2,  0, +1, +1, +1),  # East:  wall right + corner below-right
        (4, +1,  0, +1, -1),  # South: wall below + corner below-left
        (8,  0, -1, -1, -1),  # West:  wall left  + corner above-left
    ]

    sol_move = {
        "N": (-1, 0),  # North: row - 1
        "E": (0, +1),  # East:  col + 1
        "S": (+1, 0),  # South: row + 1
        "W": (0, -1),  # West:  col - 1
    }

    wall_colors = [Presets.WHITE, Presets.GREEN, Presets.YELLOW, Presets.CYAN]

    def __init__(self, width: int, height: int, entry: tuple[int, int], exit: tuple[int, int], cells: list[int], solution: str):
        self.width = width
        self.height = height
        # self.entry = entry
        # self.exit_ = exit
        self.cells = cells
        self.solution = solution

        self.color_index = 0
        self.show_path = False
        self.grid_width = width * 2 + 1
        self.grid_height = height * 2 + 1
        self.entry_y = entry[1] * 2 + 1
        self.entry_x = entry[0] * 2 + 1
        self.exit_y = exit[1] * 2 + 1
        self.exit_x = exit[0] * 2 + 1

    def render_maze(self) -> None:
        try:
            print("\033c", end="")
            colored_wall = f"{self.wall_colors[self.color_index].value}{Presets.WALL.value}{Presets.RESET.value}"

            # GRID
            grid: list[list[str]] = [
                [Presets.PATH.value for _ in range(self.grid_width)] for _ in range(self.grid_height)
            ]

            for row in range(self.height):
                for col in range(self.width):
                    cell = self.cells[row * self.width + col]
                    y = row * 2 + 1
                    x = col * 2 + 1

                    for bit, wall_y, wall_x, corner_y, corner_x in self.walls:
                        if cell & bit:
                            grid[y + wall_y][x + wall_x] = colored_wall
                            grid[y + corner_y][x + corner_x] = colored_wall

                    # Fully closed
                    if cell == 15:
                        grid[y][x] = f"{Presets.GREY.value}{Presets.WALL.value}{Presets.RESET.value}"

            # ENTRY/EXIT
            grid[self.entry_y][self.entry_x] = f"{Presets.MAGENTA.value}{Presets.WALL.value}{Presets.RESET.value}"
            grid[self.exit_y][self.exit_x] = f"{Presets.RED.value}{Presets.WALL.value}{Presets.RESET.value}"

            # SOLUTION PATH
            if self.show_path:
                sol_y = self.entry_y
                sol_x = self.entry_x
                for step in self.solution:
                    step_y, step_x = self.sol_move[step]

                    # Wall unit
                    sol_y += step_y
                    sol_x += step_x
                    grid[sol_y][sol_x] = f"{Presets.BLUE.value}{Presets.WALL.value}{Presets.RESET.value}"

                    # Cell unit
                    sol_y += step_y
                    sol_x += step_x
                    grid[sol_y][sol_x] = f"{Presets.BLUE.value}{Presets.WALL.value}{Presets.RESET.value}"

                    # Draw path
                    print("\033c", end="")
                    for row_printed in grid:
                        print("".join(row_printed))
                    time.sleep(0.05)
                # return

            # DRAW
            print("\033c", end="")
            for row_printed in grid:
                print("".join(row_printed))
        except KeyboardInterrupt:
            print("Bye!\n")
            exit(1)
        except Exception as e:
            print("Got an error while rendering:", e)


# hex_strings = [
#     "9", "5", "1", "5", "3", "9", "1", "5", "3", "9", "5", "5", "1", "7", "9", "5", "1", "5", "1", "1", "5", "1", "1", "5", "3",
#     "E", "B", "A", "B", "A", "E", "8", "1", "2", "8", "5", "3", "C", "1", "4", "1", "2", "B", "A", "8", "1", "2", "8", "1", "2",
#     "9", "6", "A", "8", "4", "1", "6", "A", "8", "4", "5", "4", "5", "4", "1", "2", "A", "C", "4", "2", "8", "2", "C", "2", "A",
#     "C", "3", "A", "8", "3", "8", "1", "6", "A", "9", "3", "9", "5", "3", "8", "4", "4", "5", "3", "A", "8", "2", "D", "0", "2",
#     "9", "6", "8", "4", "2", "A", "8", "5", "2", "A", "C", "0", "7", "A", "A", "D", "1", "3", "A", "8", "2", "8", "3", "C", "2",
#     "C", "1", "2", "9", "6", "C", "4", "3", "A", "A", "B", "8", "3", "A", "A", "9", "2", "A", "A", "8", "6", "8", "6", "B", "A",
#     "9", "2", "E", "8", "5", "3", "9", "6", "8", "4", "2", "8", "4", "4", "4", "6", "8", "2", "A", "C", "1", "2", "9", "0", "2",
#     "A", "C", "3", "8", "1", "4", "4", "5", "2", "F", "A", "8", "3", "F", "F", "F", "8", "2", "C", "5", "2", "C", "4", "2", "A",
#     "8", "5", "6", "8", "4", "1", "1", "7", "A", "F", "C", "6", "8", "5", "7", "F", "A", "C", "1", "3", "8", "3", "D", "0", "6",
#     "C", "5", "3", "A", "D", "0", "4", "3", "A", "F", "F", "F", "A", "F", "F", "F", "8", "5", "6", "A", "A", "8", "1", "4", "3",
#     "9", "1", "4", "4", "1", "2", "9", "4", "2", "9", "7", "F", "A", "F", "D", "5", "0", "1", "1", "4", "2", "C", "6", "B", "A",
#     "A", "A", "9", "1", "2", "A", "C", "3", "8", "4", "3", "F", "A", "F", "F", "F", "8", "2", "8", "5", "6", "D", "5", "2", "A",
#     "8", "4", "2", "A", "8", "6", "9", "2", "A", "9", "2", "B", "8", "5", "1", "7", "C", "4", "4", "5", "1", "5", "5", "2", "A",
#     "8", "1", "6", "A", "C", "3", "8", "4", "4", "6", "8", "2", "8", "5", "2", "9", "3", "9", "1", "7", "A", "9", "5", "4", "2",
#     "C", "4", "1", "6", "9", "2", "8", "5", "1", "3", "C", "4", "4", "3", "A", "8", "2", "8", "4", "5", "6", "C", "3", "B", "A",
#     "9", "1", "4", "1", "6", "A", "A", "9", "2", "C", "3", "9", "3", "A", "8", "2", "8", "0", "1", "5", "5", "3", "A", "A", "A",
#     "A", "8", "1", "2", "9", "2", "A", "A", "8", "1", "4", "6", "8", "2", "C", "6", "A", "8", "6", "9", "3", "C", "6", "A", "A",
#     "A", "8", "4", "4", "2", "C", "6", "C", "2", "C", "1", "1", "6", "8", "5", "5", "2", "C", "1", "6", "A", "9", "5", "4", "2",
#     "8", "6", "9", "5", "6", "9", "5", "1", "6", "9", "2", "C", "1", "4", "5", "5", "4", "1", "6", "9", "2", "8", "5", "5", "2",
#     "C", "5", "4", "5", "5", "4", "5", "4", "5", "6", "C", "5", "4", "5", "5", "5", "5", "4", "5", "4", "4", "4", "5", "5", "6",
# ]
# cells = [int(ch, 16) for ch in hex_strings]

# solution = [2, 3, 2, 2, 2, 1, 1, 2, 1, 1, 1]

##############################################################################



# try:
#     while True:
#         render_maze(WALL_COLORS[color_index], show_path)
#         print("\n=== A-Maze-ing ===")
#         print("1. Re-generate a new maze")
#         print("2. Show/Hide path from entry to exit")
#         print("3. Rotate maze colors")
#         print("4. Quit")
#         choice = input("Choice? (1-4): ")

#         # if choice == "1":
#         #     ft_maze_gen()
#         if choice == "2":
#             show_path = not show_path
#         elif choice == "3":
#             color_index = (color_index + 1) % len(WALL_COLORS)
#         elif choice == "4":
#             print("Bye!")
#             break
#         else:
#             continue
# except KeyboardInterrupt:
#     print("\nBye!")