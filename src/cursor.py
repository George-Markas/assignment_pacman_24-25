import sys


# static
def replace(char):
    """Replace character at cursor position."""
    sys.stdout.write(char)
    sys.stdout.flush()

# static
def set_pos(row, col):
    """Move cursor to a specific position"""
    sys.stdout.write(f'\033[{row};{col}H')
    sys.stdout.flush()


class Cursor:
    __slots__ = ("CURSOR_UP", "CURSOR_DOWN", "CURSOR_RIGHT", "CURSOR_LEFT", "SAVE_POSITION", "RESTORE_POSITION",
                "DELETE_CHAR", "INSERT_CHAR")

    def __init__(self):
        self.CURSOR_UP = '\033[A'
        self.CURSOR_DOWN = '\033[B'
        self.CURSOR_RIGHT = '\033[C'
        self.CURSOR_LEFT = '\033[D'
        self.SAVE_POSITION = '\033[s'
        self.RESTORE_POSITION = '\033[u'
        self.DELETE_CHAR = '\033[P'
        self.INSERT_CHAR = '\033[@'


    def move(self, up=0, down=0, right=0, left=0):
        """Move cursor in any direction."""
        if up:
            sys.stdout.write(self.CURSOR_UP * up)
        if down:
            sys.stdout.write(self.CURSOR_DOWN * down)
        if right:
            sys.stdout.write(self.CURSOR_RIGHT * right)
        if left:
            sys.stdout.write(self.CURSOR_LEFT * left)
        sys.stdout.flush()


    def save_pos(self):
        """Save current cursor position."""
        sys.stdout.write(self.SAVE_POSITION)
        sys.stdout.flush()


    def restore_pos(self):
        """Restore previously saved cursor position."""
        sys.stdout.write(self.RESTORE_POSITION)
        sys.stdout.flush()


    def delete(self, count = 1):
        """Delete character(s) at cursor position, defaults to deleting one character if not specified"""
        sys.stdout.write(self.DELETE_CHAR * count)
        sys.stdout.flush()


    def insert(self, char):
        """Insert a character at cursor position."""
        sys.stdout.write(self.INSERT_CHAR) # Make space for insertion
        sys.stdout.write(char)
        sys.stdout.flush()