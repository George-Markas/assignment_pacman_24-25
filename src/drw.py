import os
from time import sleep


def clear_screen():
    # windows
    if os.name == 'nt':
        _ = os.system('cls')
    # *nix
    else:
        _ = os.system('clear')


class Pacman_colors:
    pacman = "\033[1;33m"
    fruit = "\033[0;31m"
    fruit_poisoned = "\033[0;35m"
    ansi_reset = "\033[0m"

    @classmethod
    def ansi_color(cls, input, color_name):
        try:
            return getattr(cls, color_name) + input + cls.ansi_reset
        except ValueError:
            return None # Invalid color


# Color list items, yellow for Pacman, red for fruit and magenta for poisoned fruit
def color_items(string) -> str:
    row = ""
    for char in string:
        match char:
            case 'p':
                row += f"{Pacman_colors.ansi_color(char, "pacman")}"
            case 'f':
                row += f"{Pacman_colors.ansi_color(char, "fruit")}"
            case 'd':
                row += f"{Pacman_colors.ansi_color(char, "fruit_poisoned")}"
            case _:
                row += char # do nothing
    return row


# From i-th list within the input list, return a character if there is one or a space if there is no character
def pick_non_empty(input: list[list[str]], index) -> str:
    output = ' '
    for i, element in enumerate(input[index]):
        if element:
            output = element

    return output


# Draw a grid containing the character (or space in the absence of a character) of each list in input
def draw_grid(input: list[list[str]], clear_on_update: bool = False) -> None:
    # clear terminal with each call if enabled, sleep is used to pseudo-animate the grid
    if clear_on_update: sleep(0.25) or clear_screen()

    # Top row
    header = "┌" + "┬".join(f"{i}──" for i in range(1, len(input) + 1)) + "┐"

    # Line separated contents
    values = ''
    for i in range(0, len(input), 1):
        result = pick_non_empty(input, i)
        values += result

    grid_row = "│ " + " │ ".join(values)+ " │"
    grid_row = color_items(grid_row)

    # Bottom row
    footer = "└" + "┴".join("───" for _ in input) + "┘\n"

    print(f"{header}\n{grid_row}\n{footer}")