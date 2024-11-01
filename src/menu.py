import sys
import keyboard
import time
from drw import clear_screen
from enum import Enum
from cursor import Cursor


Method = Enum("Method", ["BestFS", "DFS", "BFS"])


def get_method_name_from_opt(option):
    try:
        return Method(option + 1).name
    except ValueError:
        return None


def draw_interactive_menu():
    print("\n ┌Select method──────────────┐\n"
          " │                           │\n"
          " │    1. BestFS      (*)     │\n"
          " │    2. DFS         ( )     │\n"
          " │    3. BestFS      ( )     │\n"
          " │                           │\n"
          " └Nxt↓─Prv↑─────────Sel⏎─Ext␛┘\n", end="")


def method_select(opt) -> None:
    #   Changing the selected method works as follows:
    #       1. Clear asterisk on current position.
    #       2. Set cursor position one line up/down corresponding to the newly selected method.
    #       3. Replace the space with the asterisk at the new position.
    #       4. Move cursor one space to the left to account for the asterisk insertion.

    match opt:
        case 0:
            Cursor.replace(' ')
            Cursor.set_pos(4, 23)
            Cursor.replace('*')
            Cursor.move(left = 1)
        case 1:
            Cursor.replace(' ')
            Cursor.set_pos(5,23)
            Cursor.replace('*')
            Cursor.move(left = 1)
        case 2:
            Cursor.replace(' ')
            Cursor.set_pos(6, 23)
            Cursor.replace('*')
            Cursor.move(left = 1)


def draw_simple_menu() -> None:
    print(" ┌Select method──────────────┐\n"
          " │                           │\n"
          " │         1. BestFS         │\n"
          " │         2. DFS            │\n"
          " │         3. BFS            │\n"
          " │         0. \x1B[3mexit\x1B[0m           │\n"
          " │                           │\n"
          " └───────────────────────────┘\n"
          "  Input number: ", end = "")


def show_help() -> None:
    print("\npacman [\x1B[3mFLAG\x1B[0m]...[\x1B[3mOPTION\x1B[0m]...\n\n"
          "-m, --menu\n\n\tStart the program with a menu, defaults to interactive. Options: \x1B[3msimple\x1B[0m\n\n"
          "-s, --silent\n\n\tSkip all menus and run directly by providing a method as an argument. Options: \x1B[3mbfs, dfs, bestfs\x1B[0m\n\n"
          "-h, --help\n\n\tDisplay help page.\n\n"
          "<none>\n\n\tRuns outright by defaulting to BFS.\n")


def menu_interactive():
    opt: int = 0
    clear_screen()
    draw_interactive_menu()
    Cursor.set_pos(4, 23) # Default position (option 1)
    Cursor.hide()
    while True:
        if keyboard.is_pressed("up"):
            # If 2nd or 3rd is selected, go to previous, else wrap around to last.
            if opt in (1, 2):
                opt -= 1
            else:
                opt = 2
            method_select(opt)
            time.sleep(0.1)
        elif keyboard.is_pressed("down"):
            # If 1st or 2nd is selected, go to next, else wrap around to first
            if opt in (0, 1):
                opt += 1
            else:
                opt = 0
            method_select(opt)
            time.sleep(0.1)
        elif keyboard.is_pressed("enter"):
            return get_method_name_from_opt(opt)
        elif keyboard.is_pressed("esc"):
            clear_screen()
            exit(-1)


def menu_simple():
    draw_simple_menu()
    opt = int(input())
    match opt:
        # opt - 1 because get_method_name_from_opt counts from 0
        case 1:
            return get_method_name_from_opt(opt - 1)
        case 2:
            return get_method_name_from_opt(opt - 1)
        case 3:
            return get_method_name_from_opt(opt - 1)
        case 0:
            clear_screen()
            exit(-1)


def start_menu():
    if len(sys.argv) > 1:
        match sys.argv[1]:
            case ("--menu" | "-m"):
                if len(sys.argv) < 3 or not sys.argv[2]:  # Defaults to interactive if no argument is given for -m
                    method = menu_interactive()
                    Cursor.show()
                    return method
                elif sys.argv[2] == "simple":
                    method = menu_simple()
                    return method
                else:
                    print("\n\033[0;31mError: \033[0minvalid menu option\n")
            case ("--help" | "-h"):
                show_help()
            case ("--silent" | "-s"):
                try:
                    sys.argv[2]
                except IndexError:
                    print("\n\033[0;31mError: \033[0msecond argument is missing\n")
                    sys.exit(-1)

                if sys.argv[2] == "bfs":
                    return "BFS"
                elif sys.argv[2] == "dfs":
                    return "DFS"
                elif sys.argv[2] == "bestfs":
                    return "BestFS"
                else:
                    print("\n\033[0;31mError: \033[0minvalid method\n")
            case _:
                print("\n\033[0;31mError: \033[0m invalid argument(s)\n")
    else:
        return "BFS" # Defaults to BFS if no arguments are given