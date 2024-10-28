"""----------------------------------------------------------------------------
******** Search Code for DFS  and other search methods
******** (expanding front and extending queue)
******** author:  AI lab
********
******** Κώδικας για DFS και άλλες μεθόδους αναζήτησης
******** (επέκταση μετώπου και διαχείριση ουράς)
******** Συγγραφέας: Εργαστήριο ΤΝ
"""


from random import randint
from copy import deepcopy

import sys

from menu import start_menu
from drw import draw_grid

sys.setrecursionlimit(10**6)
sys.tracebacklimit = 0 # To reduce the footprint of the annoying queue warning, remove when fixed

""" Helper functions for checking operator's conditions """


def can_eat(state):
    for i in state:
        if i[0] == "p":
            return i[1] == "d" or i[1] == "f"
    return False  # Fail safe


def can_move_right(state):
    return not state[len(state) - 1][0] == "p"


def can_move_left(state):
    return not state[0][0] == "p"


""" Operator function: eat, move right, move left """

rndm_queue = []

def eat(state, is_front = True) -> None:
    global rndm_queue
    if not can_eat(state):
        return
    pacman_pos = -1
    for i in range(len(state)):
        if state[i][0] == "p":
            pacman_pos = i
            break
    if state[pacman_pos][1] == "f":
        state[pacman_pos][1] = ""
    elif state[pacman_pos][1] == "d":
        have_fruits_or_player: list[int] = []
        pos: int = 0
        for i in range(len(state)):
            if state[i][1] == "f" or state[i][1] == "d":
                have_fruits_or_player.append(i)
            if state[i][0] == "p":
                have_fruits_or_player.append(i)
                pos = i

        valid_spaces: int = len(state) - len(have_fruits_or_player)
        random_space = -1
        if is_front:
            random_space: int = randint(0, valid_spaces)
            rndm_queue.append(random_space)
        else:
            random_space = rndm_queue.pop(0)

        for i in have_fruits_or_player:
            if i >= random_space:
                random_space += 1
        state[random_space][1] = "f"
        state[pos][1] = ""
    return


def move_right(state) -> list[list[str]] | None:
    if can_move_right(state):
        for i in range(len(state) - 1):
            if state[i][0] == "p":
                state[i][0] = ""
                state[i + 1][0] = "p"
                return state
    else:
        return None


def move_left(state) -> list[list[str]] | None:
    if can_move_left(state):
        for i in range(1, len(state)):
            if state[i][0] == "p":
                state[i][0] = ""
                state[i - 1][0] = "p"
                return state
    else:
        return None


""" Function that checks if current state is a goal state """


def is_goal_state(state):
    """Return true if state is a goal state
    
    Example:
    -------
    >>> is_goal_state([["p", ""], ["", ""]])
    True
    >>> is_goal_state([["p", ""], ["", "f"]])
    False
    """
    for s in state:
        if s[1] != "":
            return False
    return True


""" Function that finds the children of current state """


def find_children(state: list[list[str]]) -> list[list[list[str]]]:
    """Find the blocks next to Pacman"""
    children = []

    left_state = deepcopy(state)
    child_left = move_left(left_state)

    right_state = deepcopy(state)
    child_right = move_right(right_state)

    if child_left is not None:
        children.append(child_left)

    if child_right is not None:
        children.append(child_right)
    return children


""" ----------------------------------------------------------------------------
**** FRONT
**** Διαχείριση Μετώπου
"""

""" ----------------------------------------------------------------------------
** initialization of front
** Αρχικοποίηση Μετώπου
"""


def make_front(state):
    """Make front :)"""
    return [state]


""" ----------------------------------------------------------------------------
**** expanding front
**** επέκταση μετώπου    
"""

# Kept for reference
#
# def print_front(f):
#     """Print front :)"""
#     for i in f:
#         print(i)

# drw.py compatible print_front
def print_front(f :list[list[list[str]]]):
    for i in range(0, len(f), 1):
        draw_grid(f[i], False)

def count_fruit(state):
    """Count fruits for BestFS"""
    cntr = 0
    for f in state:
        if f[1] == "f":
            cntr += 1
        elif f[1] == "d":
            cntr += 2
    return cntr

def expand_front(front: list[list[list[str]]], method):
    """Calculate the next parts of the front base on the given method

    Parameters:
    front -- Initial front state
    method -- The method that will use the function
    """
    if method == "DFS":
        if front:
            print("\033[1;32mFront:\033[0m")
            print_front(front)
            node = front.pop(0)
            for child in find_children(node):
                eat(child)
                front.insert(0, child)

    elif method == "BFS":
        if front:
            print("\033[1;32mFront:\033[0m")
            print_front(front)
            node = front.pop(0)
            for child in find_children(node):
                eat(child)
                front.append(child)

    elif method=='BestFS':
        if front:
            print("\033[1;32mFront:\033[0m")
            print_front(front)
            node = front.pop(0)
            for child in find_children(node):
                eat(child)
                fruit_count = count_fruit(child)
                inserted = False
                for i in range(len(front)):
                    if count_fruit(front[i]) > fruit_count:
                        front.insert(i, child)
                        inserted = True
                        break
                if not inserted:
                    front.append(child)

    # else: "other methods to be added"

    return front


""" ----------------------------------------------------------------------------
**** QUEUE
**** Διαχείριση ουράς
"""

""" ----------------------------------------------------------------------------
** initialization of queue
** Αρχικοποίηση ουράς
"""


def make_queue(state):
    return [[state]]


""" ----------------------------------------------------------------------------
**** expanding queue
**** επέκταση ουράς
"""

# Kept for reference
#
# def print_queue(q):
#     for i in q:
#         for j in i:
#             print(j)

# draw_grid() compatible print queue
def print_queue(q):
    for i in range(0, len(q), 1):
        print_front(q[i])

def extend_queue(
    queue: list[list[list[list[str]]]],
    method: str
) -> list[list[list[list[str]]]]:
    """Φτιάχνει τη σειρά από την αρχική στην τελική/μερική κατάσταση"""

    # Δε θα ήταν καλύτερο το queue copy να αρχικοποιείται εδώ έξω από τα ifs για να αποφευχθεί το warning;
    # queue_copy = deepcopy(queue)

    if method == "DFS":
        print("\033[1;36mQueue:\033[0m")
        print_queue(queue)
        node = queue.pop(0)
        queue_copy = deepcopy(queue)
        children = find_children(node[-1])
        for child in children:
            eat(child, False)
            path = deepcopy(node)
            path.append(child)
            queue_copy.insert(0, path)

    elif method=='BFS':
        print("\033[1;36mQueue:\033[0m")
        print_queue(queue)
        node = queue.pop(0)
        queue_copy = deepcopy(queue)
        children = find_children(node[-1])
        for child in children:
            eat(child, False)
            path = deepcopy(node)
            path.append(child)
            queue_copy.append(path)

    elif method=='BestFS':
        print("\033[1;36mQueue:\033[0m")
        print_queue(queue)
        node = queue.pop(0)
        queue_copy = deepcopy(queue)
        children = find_children(node[-1])
        for child in children:
            eat(child, False)
            path = deepcopy(node)
            path.append(child)

            fruit_count = count_fruit(child)
            inserted = False
            for i in range(len(queue_copy)):
                if count_fruit(queue_copy[i][-1]) > fruit_count:
                    queue_copy.insert(i, path)
                    inserted = True
                    break
            if not inserted:
                queue_copy.append(path)
    # else: "other methods to be added"

    # WARN: IGNORE WARNING HERE. PLEASE!!!
    return queue_copy


""" ----------------------------------------------------------------------------
**** Problem depending functions
**** ο κόσμος του προβλήματος (αν απαιτείται) και υπόλοιπες συναρτήσεις σχετικές με το πρόβλημα

  #### to be  added ####
"""

""" ----------------------------------------------------------------------------
**** Basic recursive function to create search tree (recursive tree expansion)
**** Βασική αναδρομική συνάρτηση για δημιουργία δέντρου αναζήτησης (αναδρομική επέκταση δέντρου)
"""


def find_solution(front, queue, closed, method) -> None:
    if not front:
        print("\033[1;31mNo solution.\033[0m")

    elif front[0] in closed:
        new_front = deepcopy(front)
        new_front.pop(0)
        new_queue = deepcopy(queue)
        new_queue.pop(0)
        find_solution(new_front, new_queue, closed, method)

    elif is_goal_state(front[0]):
        print("\033[1;34m  This is the solution: \033[0m")
        print_front(queue[0])

    else:
        closed.append(front[0])
        front_copy = deepcopy(front)
        front_children = expand_front(front_copy, method)
        queue_copy = deepcopy(queue)
        queue_children = extend_queue(queue_copy, method)
        closed_copy = deepcopy(closed)
        find_solution(front_children, queue_children, closed_copy, method)


"""" ----------------------------------------------------------------------------
** Executing the code
** κλήση εκτέλεσης κώδικα
"""


def main():
    initial_state = [
        ["", "d"],
        ["", "f"],
        ["p", ""],
        ["", ""],
        ["", "f"],
        ["", ""],
    ]

    method = start_menu() # Defaults to BFS (the fastest)

    # Kept for reference
    #
    # if len(sys.argv) > 1:
    #     method = sys.argv[1]
    #     if method not in ["DFS", "BFS", "BestFS"]:
    #         raise ValueError(f"Not an Implemented method: {method}")

    """ ----------------------------------------------------------------------------
    **** starting search
    **** έναρξη αναζήτησης
    """
    find_solution(make_front(initial_state), make_queue(initial_state), [], method)


if __name__ == "__main__":
    main()
