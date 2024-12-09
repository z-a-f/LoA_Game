from enum import Enum
import numpy as np

from linesofaction.piece import Piece
from linesofaction import _utils


class GameEndState(Enum):
    '''Game end states.'''
    TIE = 0
    WIN1 = 1
    WIN2 = 2
    CONTINUE = 3


class GameRules:
    '''
    Rules:
        * The game is played on an NxN board.
        * Each player has 2N-4 pieces.
        * The pieces are placed on the first and last rows for Player 1
          and the first and last columns for Player 2.
        * The corner positions are initially empty.
        * The objective is to connect all of your pieces into a single group.
        * A player can move a piece horizontally, vertically, or diagonally.
        * The number of steps a piece can move is equal to the total number of pieces
          (both players') on that piece's current line (rank, file, or diagonal).
        * A player can capture an opponent's piece by moving onto its position.
        * A piece cannot move over enemy pieces, but it can jump over friendly pieces.
    '''
    kRows = 8
    kCols = 8
    kNumPlayers = 2

    # === Board Validation ===
    def is_valid_board(self, board):
        '''Checks if the board configuration is valid.'''
        return (self._is_valid_board_size(board)
            and self._is_valid_num_players(board)
            and self._is_valid_num_pieces(board))

    def is_valid_init_board(self, board):
        '''Checks if the board is valid for the initial game state.'''
        return (self.is_valid_board(board)
            and self._is_empty_corners(board)
            and self._is_initial_player_positions(board))

    def _is_valid_board_size(self, board):
        return board.rows == self.kRows and board.cols == self.kCols

    def _is_valid_num_players(self, board):
        return len(board.players) == self.kNumPlayers

    def _is_valid_num_pieces(self, board):
        n1 = board.count(board.players[0])
        n2 = board.count(board.players[1])
        # For the standard LOA rules: each player starts with 2N-4 pieces for an NxN board.
        # For an 8x8 board, each player has 12 pieces. The code places them as per the initialization rules.
        # We just check that counts make sense (non-empty, etc.).
        # The conditions in the provided code might be too strict or lenient, adjust as needed:
        return n1 > 0 and n2 > 0 and n1 <= (2 * board.cols - 4) and n2 <= (2 * board.rows - 4)

    def _is_empty_corners(self, board):
        return (board.peek(0, 0) == Piece.EMPTY
            and board.peek(0, -1) == Piece.EMPTY
            and board.peek(-1, 0) == Piece.EMPTY
            and board.peek(-1, -1) == Piece.EMPTY)

    def _is_initial_player_positions(self, board):
        # Checks that initial pieces are placed as per standard Lines of Action rules:
        # Player[0] on first and last rows (except corners),
        # Player[1] on first and last columns (except corners).
        return ((board.board[[0, -1], 1:-1] == board.players[0]).all()
            and (board.board[1:-1, [0, -1]] == board.players[1]).all()
            and board.count(board.players[0]) == 2 * (board.cols - 2)
            and board.count(board.players[1]) == 2 * (board.rows - 2))

    # === Movement Checks and Rules ===
    def is_movable(self, board, position, current_player):
        '''Checks if the piece at the given position is movable.'''
        piece = board.peek(*position)
        return piece == current_player and piece != Piece.EMPTY

    def get_valid_steps(self, board, position, current_player):
        '''Returns the valid steps (final positions) for the piece at the given position.'''

        # Count pieces along each line (horizontal, vertical, diagonal, antidiagonal)
        # These counts determine how far the piece can move.
        num_pieces = {'n': 0, 's': 0, 'e': 0, 'w': 0, 'ne': 0, 'nw': 0, 'se': 0, 'sw': 0}

        # For each orientation, count how many pieces are on that line
        # line_coords returns all coords along that line (including the position itself)
        for orient in 'hvda':
            line = list(_utils.line_coords(board.board.shape, position, orient))
            pieces = board.board[tuple(zip(*line))]
            line_count = int((pieces != Piece.EMPTY).sum())

            # Assign the line_count to the appropriate directions:
            # h: east/west
            # v: north/south
            # d: northeast/southwest (main diagonal)
            # a: northwest/southeast (anti-diagonal)
            if orient == 'h':
                num_pieces['e'] = line_count
                num_pieces['w'] = line_count
            elif orient == 'v':
                num_pieces['n'] = line_count
                num_pieces['s'] = line_count
            elif orient == 'd':
                num_pieces['ne'] = line_count
                num_pieces['sw'] = line_count
            elif orient == 'a':
                num_pieces['nw'] = line_count
                num_pieces['se'] = line_count

        # Now get all lines of sight including obstacles.
        # We include obstacles to ensure no jumping over enemy pieces.
        obstacle_positions = board.get_positions(~current_player)
        lines_of_sight = _utils.all_line_of_sight_coords(
            board.board.shape,
            position,
            obstacle_positions,
            include_obstacles=True
        )

        valid_steps = set()

        # For each direction, find squares exactly num_pieces[direction] steps away
        # Directions here are keys in num_pieces: n,s,e,w,ne,nw,se,sw
        # lines_of_sight already includes direction keys (like 'n','s','e','w', etc.)
        for direction, steps_required in num_pieces.items():
            los_coords = lines_of_sight.get(direction, set())
            for coord in los_coords:
                # The Manhattan or Chebyshev distance in LOA is max of row diff or col diff
                # to determine steps along a line.
                if max(abs(coord[0]-position[0]), abs(coord[1]-position[1])) == steps_required:
                    valid_steps.add(coord)

        # Remove positions occupied by our own pieces, as you cannot end on your own piece
        # (although you can jump over them if line_of_sight allows)
        player_positions = set(board.get_positions(current_player))
        valid_steps -= player_positions

        # You can land on empty squares or opponent squares. Opponent squares represent captures.
        return valid_steps

    # === Game Checks ===
    def is_game_over(self, board):
        '''Checks if the game is over and returns the game state.'''
        connected1 = self._all_connected(board, board.players[0])
        connected2 = self._all_connected(board, board.players[1])

        if connected1 and connected2:
            return GameEndState.TIE
        elif connected1:
            return GameEndState.WIN1
        elif connected2:
            return GameEndState.WIN2
        else:
            return GameEndState.CONTINUE

    def _all_connected(self, board, player):
        '''Checks if all pieces of the given player are connected (forming a single group).'''
        positions = board.get_positions(player)
        if not positions:
            # If no pieces are found (should not happen in a normal game), consider them not connected.
            return False

        visited = set()
        stack = [positions[0]]
        piece_positions = set(positions)

        while stack:
            pos = stack.pop()
            if pos in visited:
                continue
            visited.add(pos)

            # Add neighbors that belong to the same player
            for nbr in self._get_neighbors(board, pos):
                if nbr in piece_positions and nbr not in visited:
                    stack.append(nbr)

        return len(visited) == len(piece_positions)

    def _get_neighbors(self, board, position):
        '''Return all orthogonal and diagonal neighbors of position.'''
        # In Lines of Action, connectivity is typically considered with the 8 surrounding squares.
        # Adjust if different adjacency rules apply.
        row, col = position
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]
        neighbors = []
        for dr, dc in directions:
            r, c = row+dr, col+dc
            if 0 <= r < board.rows and 0 <= c < board.cols:
                neighbors.append((r, c))
        return neighbors
