import sys


class Cursor:
    CURSOR_UP = '\033[A'
    CURSOR_DOWN = '\033[B'
    CURSOR_RIGHT = '\033[C'
    CURSOR_LEFT = '\033[D'
    SAVE_POSITION = '\033[s'
    RESTORE_POSITION = '\033[u'
    DELETE_CHAR = '\033[P'
    INSERT_CHAR = '\033[@'


    @staticmethod
    def move(up=0, down=0, right=0, left=0) -> None:
        """Move cursor in any direction."""
        if up:
            sys.stdout.write(Cursor.CURSOR_UP * up)
        if down:
            sys.stdout.write(Cursor.CURSOR_DOWN * down)
        if right:
            sys.stdout.write(Cursor.CURSOR_RIGHT * right)
        if left:
            sys.stdout.write(Cursor.CURSOR_LEFT * left)
        sys.stdout.flush()


    @staticmethod
    def save_pos() -> None:
        """Save current cursor position."""
        sys.stdout.write(Cursor.SAVE_POSITION)
        sys.stdout.flush()


    @staticmethod
    def restore_pos() -> None:
        """Restore previously saved cursor position."""
        sys.stdout.write(Cursor.RESTORE_POSITION)
        sys.stdout.flush()


    @staticmethod
    def delete(count = 1) -> None:
        """Delete character(s) at cursor position, defaults to deleting one character if not specified."""
        sys.stdout.write(Cursor.DELETE_CHAR * count)
        sys.stdout.flush()


    @staticmethod
    def insert(char) -> None:
        """Insert a character at cursor position."""
        sys.stdout.write(Cursor.INSERT_CHAR) # Make space for insertion
        sys.stdout.write(char)
        sys.stdout.flush()


    @staticmethod
    def replace(char) -> None:
        """Replace character at cursor position."""
        sys.stdout.write(char)
        sys.stdout.flush()


    @staticmethod
    def set_pos(row, col) -> None:
        """Move cursor to a specific position"""
        sys.stdout.write(f'\033[{row};{col}H')
        sys.stdout.flush()


    @staticmethod
    def hide() -> None:
        """Hide cursor."""
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()


    @staticmethod
    def show() -> None:
        """Unhide cursor."""
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
