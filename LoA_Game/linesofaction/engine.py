import numpy as np

from linesofaction.board import Board
# from linesofaction.piece import Piece
from linesofaction import _utils

class GameEngine:
    r'''Lines of Action game engine class.

    This class is responsible for managing the game state and rules.

    Args:
        board (Board): Board object for the game.
            If None, a new 8x8 board is created.
    '''
    def __init__(self, board: Board=None):
        if board is None:
            board = Board(rows=8, cols=8)
        self.board = board
        self.current_player = self.board.players[0]
        self._selected_position = None  # We will use a property to make sure we know which piece is at the selected position
        self.winner = None
    
    def reset(self):
        '''Resets the game to the initial state.'''
        self.board._init_board()._init_pieces()
        self.current_player = self.board.players[0]
        self._selected_position = None
        self.winner = None
        return self
    
    # === Position Selection ===
    @property
    def selected(self):
        if self._selected_position is None:
            piece = None
        else:
            piece = self.board.peek(*self._selected_position)
        return {'position': self._selected_position, 'piece': piece}

    # def select(self, position):
    #     self._selected_position = position

    def select(self, position=None, player=True, reset=True):
        '''Marks the position for further action
        
        Args:
            position (tuple): Position to select.
                If None, the selected position is reset.
            player (bool): If True, only the position with the player's piece can be selected.
            reset (bool): If True, resets the selected position if the position is not valid.
        
        Returns:
            GameEngine: self
        
        Raises:
            ValueError: If trying to select the current player and not allowing to reset.
            ValueError: If the position is empty.

        Using `select(<position>, player=False, reset=False)` is equivalent to forcing the selection of the position.
        Using `select(None, ...)` is equivalent to deselecting the position.

        | player | reset | Selected Position        | Deselecting Position if Already Selected  |
        |--------|-------|--------------------------|-------------------------------------------|
        | False  | False | Any                      | Never                                     |
        | False  | True  | Any Players's Piece      | On empty position                         |
        | True   | False | Current Player's Piece   | Raise Value Error                         |
        | True   | True  | Current Player's Piece   | On any other position                     |      
        '''
        if position is None:
            self._selected_position = None
            return self
        
        if not player and not reset:
            self._selected_position = position
        elif not player and reset:
            if self.board.is_player(position):
                self._selected_position = position
            else:
                self._selected_position = None
        elif player and not reset:
            if self.board.is_player(position, self.current_player):
                self._selected_position = position
            else:
                raise ValueError('The position is not your piece.')
        elif player and reset:
            if self.board.is_player(position, self.current_player):
                self._selected_position = position
            else:
                self._selected_position = None
        return self

    def get_positions(self):
        '''Returns the positions of the current player's pieces.'''
        return self.board.get_positions(self.current_player)
    
    # === Rules -- override these to change the rules ===

    # Rule 1: The piece can jump over the friendly pieces, but cannot jump over the enemy pieces
    def get_lines_of_sight(self):
        '''Returns the line of sight in the given direction.
        
        Returns:
            list: List of positions in the line of sight.

        Note:
            lines of sight are bidirectional/ Hence the keys are:
                'h': Horizontal
                'v': Vertical
                'd': Diagonal
                'a': Antidiagonal
        '''
        obstacles_idx = self.board.get_positions(~self.current_player)
        return _utils.all_line_of_sight_coords(self.board.shape, pivot_position=self.selected['position'], obstacle_coords=obstacles_idx)
    
    # Rule 2: The number of steps a piece can move is equal to the number of pieces on the line of the path
    def get_num_steps(self):
        '''Returns the number of steps a piece can move in each direction.
        
        Returns:
            dict: Dictionary of steps in each direction.
        
        Note:
            steps are unidirectional. Hence the keys are:
                'n', 's': Vertical Up and Down
                'e', 'w': Horizontal Right and Left
                'ne', 'sw': Diagonal North-East and South-West
                'nw', 'se': Antidiagonal North-West and South-East
        '''
        orient2dir = {
            'h': ['e', 'w'],
            'v': ['n', 's'],
            'd': ['ne', 'sw'],
            'a': ['nw', 'se']
        }
        lines_of_sight = self.get_lines_of_sight()
        step_counts = {orientation: len(coords) for orientation, coords in lines_of_sight.items()}
        return step_counts

        # for orientation, direction in orient2dir.items():
        #     steps[direction] = step_counts[orientation]
        #     valid_steps = 
        # return steps

    # === Game Play ===
    # def get_valid_moves(self):
    #     '''Returns all valid moves for the piece that is currently selected.'''
    #     if self.selected['position'] is None:
    #         raise ValueError('No piece selected.')
    #     obstacles_idx = self.board.get_positions(~self.current_player)
    #     valid_sight = self.board.all_line_of_sight_coords(self.selected['position'], obstacles_idx)  # That what the piece can see
    #     valid_steps = self.


    def move(self, position, force=False):
        '''Moves the piece at the selected position to the new position.
        
        Args:
            position (tuple): New position for the piece.
            force (bool): If True, the move is forced without checking if it is a valid move.
        
        Returns:
            GameEngine: self
        
        Raises:
            ValueError:
                - If the selected position is not valid and force is False.
                - If the selected piece is not player's own piece, and force is False
                - If the selected position is empty
        '''
        # Make sure we have a selected position
        if self.selected['position'] is None:
            raise ValueError('No piece selected.')
        # Make sure the selected piece is the current player's piece
        
        if force:
            piece = self.board.pop(self.selected['position'])
            self.board.replace(position, piece)
            return self
        elif self.selected['piece'] != self.current_player:
            raise ValueError('Cannot move the piece that is not yours.')

        # Get all valid positions
        valid_moves = self.get_valid_moves()

        return self

    def __repr__(self):
        return self.board.__repr__(active=self.selected['position'])
