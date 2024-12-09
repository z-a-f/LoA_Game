import numpy as np

from linesofaction.board import Board
from linesofaction.piece import Piece
from linesofaction import _utils
from linesofaction.rules import GameRules, GameEndState

class GameEngine:
    r'''Lines of Action game engine class.
    
    This class is responsible for:
    * Initializing and resetting the board and game state
    * Tracking the current player and selected piece
    * Validating and executing moves
    * Checking and updating the game outcome
    '''

    def __init__(self, board: Board=None):
        if board is None:
            board = Board(rows=8, cols=8)
        self.board = board
        self.rules = GameRules()
        self.current_player = self.board.players[0]
        self._selected_position = None
        self.winner = None
    
    def reset(self):
        '''Resets the game to the initial state.'''
        self.board._init_board()._init_pieces()
        self.current_player = self.board.players[0]
        self._selected_position = None
        self.winner = None
        return self
    
    @property
    def selected(self):
        '''Returns currently selected piece and its position.'''
        if self._selected_position is None:
            piece = None
        else:
            piece = self.board.peek(*self._selected_position)
        return {'position': self._selected_position, 'piece': piece}

    def select(self, position=None, player=True, reset=True):
        '''Selects or deselects a piece position.

        Args:
            position (tuple): Position to select. None to deselect.
            player (bool): If True, restrict selection to current player's pieces.
            reset (bool): If True, deselect if conditions not met.

        Returns:
            GameEngine: self
        '''
        if position is None:
            self._selected_position = None
            return self
        
        if not player and not reset:
            # Select any position, don't reset
            self._selected_position = position
        elif not player and reset:
            # If position belongs to a player piece, select it, else deselect
            if self.board.is_player(position):
                self._selected_position = position
            else:
                self._selected_position = None
        elif player and not reset:
            # Must belong to current player, no reset
            if self.board.is_player(position, self.current_player):
                self._selected_position = position
            else:
                raise ValueError('The position is not your piece.')
        elif player and reset:
            # Must belong to current player, if not deselect
            if self.board.is_player(position, self.current_player):
                self._selected_position = position
            else:
                self._selected_position = None
        return self

    def get_positions(self):
        '''Returns the positions of the current player's pieces.'''
        return self.board.get_positions(self.current_player)

    def get_valid_moves(self):
        '''Returns all valid moves for the piece that is currently selected.'''
        if self.selected['position'] is None:
            raise ValueError('No piece selected.')
        # Use the rules to get valid steps
        valid_moves = self.rules.get_valid_steps(self.board, self.selected['position'], self.current_player)
        return valid_moves

    def move(self, position, force=False):
        '''Moves the currently selected piece to the new position if valid.

        Args:
            position (tuple): Destination position
            force (bool): If True, bypasses validity checks (for testing or special scenarios).
        
        Raises:
            ValueError: If no piece selected, or the move is not valid (when not forced),
                        or if trying to move a piece that doesn’t belong to the current player.
        '''
        if self.selected['position'] is None:
            raise ValueError('No piece selected.')
        
        origin = self.selected['position']
        piece = self.selected['piece']

        if not force:
            # Check if the piece is the current player's
            if piece != self.current_player:
                raise ValueError('Cannot move a piece that is not yours.')
            
            # Check if the move is in the list of valid moves
            valid_moves = self.get_valid_moves()
            if position not in valid_moves:
                raise ValueError(f'Move to {position} is not valid.')
        
        # If forced or valid, execute the move
        # If the target square has an opponent's piece, it will be captured
        target_piece = self.board.peek(*position)
        if target_piece != Piece.EMPTY and target_piece != piece:
            # Capturing an opponent's piece
            self.board.pop(position)
        
        # Remove the piece from the original position
        moved_piece = self.board.pop(origin)
        # Place the piece in the new position
        self.board.place(position, moved_piece)

        # Deselect the piece after the move
        self._selected_position = None

        # Check if the game is over
        game_state = self.rules.is_game_over(self.board)
        if game_state == GameEndState.WIN1:
            self.winner = self.board.players[0]
        elif game_state == GameEndState.WIN2:
            self.winner = self.board.players[1]
        elif game_state == GameEndState.TIE:
            self.winner = 'TIE'
        else:
            # Game continues, switch to the next player
            self.next_turn()

        return self

    def next_turn(self):
        '''Switches the current player if the game is not over.'''
        if self.winner is not None:
            return
        # current_player is a tuple: (Piece.BLACK, Piece.RED) for example.
        # Just switch to the other player.
        p1, p2 = self.board.players
        self.current_player = p2 if self.current_player == p1 else p1

    def __repr__(self):
        return self.board.__repr__(active=self.selected['position'])
