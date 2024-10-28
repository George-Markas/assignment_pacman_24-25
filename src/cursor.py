import sys


class Cursor:
    __slot__ = ("CURSOR_UP", "CURSOR_DOWN", "CURSOR_RIGHT", "CURSOR_LEFT", "SAVE_POSITION", "RESTORE_POSITION",)

    def __init__(self):
        self.CURSOR_UP = '\033[A'
        self.CURSOR_DOWN = '\033[B'
        self.CURSOR_RIGHT = '\033[C'
        self.CURSOR_LEFT = '\033[D'
        self.SAVE_POSITION = '\033[s'
        self.RESTORE_POSITION = '\033[u'
        self.DELETE_CHAR = '\033[P'
        self.INSERT_CHAR = '\033[@'


    @classmethod
    def move(cls, instance, up=0, down=0, right=0, left=0):
        """Move cursor in any direction."""
        if up:
            sys.stdout.write(instance.CURSOR_UP * up)
        if down:
            sys.stdout.write(instance.CURSOR_DOWN * down)
        if right:
            sys.stdout.write(instance.CURSOR_RIGHT * right)
        if left:
            sys.stdout.write(instance.CURSOR_LEFT * left)
        sys.stdout.flush()


    @classmethod
    def set_pos(cls, row, col):
        """Move cursor to a specific position"""
        sys.stdout.write(f'\033[{row};{col}H')
        sys.stdout.flush()


    @classmethod
    def save_pos(cls, instance):
        """Save current cursor position."""
        sys.stdout.write(instance.SAVE_POSITION)
        sys.stdout.flush()


    @classmethod
    def restore_pos(cls, instance):
        """Restore previously saved cursor position."""
        sys.stdout.write(instance.RESTORE_POSITION)
        sys.stdout.flush()


    @classmethod
    def delete(cls, instance,  count = 1):
        """Delete character(s) at cursor position, defaults to deleting one character if not specified"""
        sys.stdout.write(instance.DELETE_CHAR * count)
        sys.stdout.flush()


    @classmethod
    def insert(cls, instance, char):
        """Insert a character at cursor position."""
        sys.stdout.write(instance.INSERT_CHAR)  # Make space
        sys.stdout.write(char)  # Write the character
        sys.stdout.flush()


    @classmethod
    def replace(cls, char):
        """Replace character at cursor position."""
        sys.stdout.write(char)
        sys.stdout.flush()