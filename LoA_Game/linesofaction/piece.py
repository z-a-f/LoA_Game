
from enum import IntEnum

class Piece(IntEnum):
    EMPTY = 0
    RED = 1
    BLACK = 2

    def color(self):
        if self == Piece.EMPTY:
            return 'white'
        else:
            return self.name.lower()
    
    def opposite(self):
        if self == Piece.RED:
            return Piece.BLACK
        elif self == Piece.BLACK:
            return Piece.RED
        else:
            return Piece.EMPTY

    def char(self, offset=None):
        # Shows a character representation of the piece
        # for empty it's just '.'
        # for others it's the first letter of the color
        offset = offset or 0
        if self == Piece.EMPTY:
            return '.' if not offset else 'O'  # Empty should not have an offset
        elif offset:
            return chr(offset - ord('a') + ord(self.name[0].lower()))
        else:
            return self.name[0].lower()

    def __invert__(self):
        return self.opposite()

    def __neg__(self):
        return self.opposite()