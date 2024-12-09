from collections.abc import Iterable
import numpy as np

from linesofaction.piece import Piece
from linesofaction import _utils
# from linesofaction._utils import make_line_mask

class Board:
    r'''Board class for Lines of Action game.

    Args:
        rows (int): Number of rows in the board.
        cols (int): Number of columns in the board.
    
    Attributes:
        rows (int): Number of rows in the board.
        cols (int): Number of columns in the board.
        players (tuple): Tuple containing the two players.
                         Player 1 is always the first element.
        board (np.ndarray): 2D numpy array representing
    
    Notes:
        * Initially Player 1 occupies the first/last row
          and Player 2 occupies the first/last column.
    '''
    def __init__(self, rows: int = 8, cols: int = 8):
        if rows < 4 or cols < 4:
            raise ValueError('Board must have at least 4 rows and 4 columns')
        self.rows = rows
        self.cols = cols
        self.board = np.empty(0, dtype=int)  # Initialize in build and place
        
        # First player is always first in the tuple
        self.players = (Piece.BLACK, Piece.RED)

        # We abstract out the board creation and piece placement
        # to make it easier to test the board class (or extend it)
        self._init_board()
        self._init_pieces()

    def _init_board(self):
        self.board = np.empty((self.rows, self.cols), dtype=int)
        self.board.fill(Piece.EMPTY)
        return self
    
    def _init_pieces(self):
        # Player 1
        self.board[[0, -1], 1:-1] = self.players[0]  # First and last rows
        # Player 2
        self.board[1:-1, [0, -1]] = self.players[1]  # First and last columns
        return self
    
    def __repr__(self, active=None):
        # For debugging purposes, implementing printing of the board
        char_map = {piece.value: piece.char() for piece in Piece}
        char_map['active'] = {piece.value: piece.char(offset=0x1f150) for piece in Piece}  # Unicode character for 'A' with a circle around it
        header, index, lines = _utils.to_lines(  # Converts the board to lines of characters that represent the board
            self.board, char_map=char_map,
            active=active,
        )
        header = '  | ' + ' '.join(header)
        separator = '--+' + '-' * (self.cols * 2)

        lines = [header, separator] + [f'{idx} | ' + ' '.join(line) for idx, line in zip(index, lines)]
        return '\n'.join(lines)
    
    # ===== Board properties =====
    def _piece_mask(self, piece):
        return self.board == piece

    def count(self, piece):
        '''Counts the number of pieces of the given type on the board.

        Args:
            piece (Piece): Piece to count.
        
        Returns:
            int: Number of pieces of the given type on the board.
        '''
        return np.sum(self._piece_mask(piece))
    

    def get_positions(self, piece):
        '''Gets the positions of the given piece on the board.

        TODO: Should this return a set?
        TODO: Is making the elements tuples necessary?

        Args:
            piece (Piece): Piece to get the positions of.
        
        Returns:
            list: List of positions where the piece is located.
        '''
        piece_locations = np.argwhere(self._piece_mask(piece))
        pos = sorted(map(tuple, piece_locations.tolist()))
        return pos
    
    # ===== Interacting with the board =====
    
    def __getitem__(self, position):
        '''Gets the piece at the given position.

        Note: This is similar to the peek method.
            The advantage of this over peek, is that this supports slicing
            and other numpy array operations.

        Args:
            position (tuple): Position to get the piece from.
        
        Returns:
            Piece: The piece at the given position.
        '''
        if isinstance(position, int):
            position = (position, ...)
        return self.peek(*position)

    def peek(self, *position):
        '''Peeks at the piece at the given position.

        Args:
            position (tuple): Position to peek at.
        
        Returns:
            Piece: The piece at the given position.
        '''
        if len(position) == 1:
            position = position[0]
        row, col = position
        piece = self.board[row, col]
        if isinstance(piece, Iterable):
            return np.array(piece, dtype=Piece)
        return Piece(piece)

    def pop(self, position):
        '''Pops the piece at the given position.

        Args:
            position (tuple): Position to pop the piece from.
        
        Returns:
            Piece: The piece at the given position.
        '''
        row, col = position
        piece = self.board[row, col]
        self.board[row, col] = Piece.EMPTY
        if isinstance(piece, Iterable):
            return np.array(piece, dtype=Piece)
        return Piece(piece)

    def place(self, position, piece):
        '''Places a piece at the given position.
        
        Args:
            position (tuple): Position to place the piece.
            piece (Piece): Piece to place.

        Raises:
            ValueError: If the position is already occupied (not empty).
            ValueError: If the piece is empty
        '''
        if np.any(piece == Piece.EMPTY):
            raise ValueError('Cannot place an empty piece. Use pop instead.')

        row, col = position
        if np.any(self.board[row, col] != Piece.EMPTY):
            raise ValueError('Position is already occupied. Use pop first.')
        self.board[row, col] = piece
        return self

    def replace(self, position, piece):
        '''Replaces a piece at the given position.
        
        This is a wrapper around pop and place.
        This raises no errors.
        '''
        self.pop(position)
        self.place(position, piece)
        return self

    # ===== Checking the board =====
    def is_piece(self, position, piece):
        '''Checks if the piece at the given position is the given piece.

        Args:
            position (tuple): Position to check.
            piece (Piece): Piece to check for.
        
        Returns:
            bool: True if the piece at the position is the given piece, False otherwise.
        '''
        if not isinstance(position, (list, tuple, slice)):
            position = (position,)
        return self.peek(*position) == Piece(piece)

    def is_empty(self, position):
        '''Checks if the position is empty.

        Args:
            position (tuple): Position to check.
        
        Returns:
            bool: True if the position is empty, False otherwise.
        '''
        return self.is_piece(position, Piece.EMPTY)

    def is_player(self, position, player=None):
        '''Checks if the piece at the position belongs to the player or if it's a player at all

        Args:
            position (tuple): Position to check.
            player (Piece): Player to check for. If None, checks for any player
        
        Returns:
            bool: True if the piece at the position belongs to the player, False otherwise.
        '''
        if player is None:
            return not self.is_empty(position)
        return self.is_piece(position, player)
    
    @property
    def shape(self):
        return self.board.shape


