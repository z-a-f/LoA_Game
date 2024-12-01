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
        * The objective is to connect all of your pieces in a single group.
        * A player can move a piece horizontally, vertically, or diagonally.
        * The number of steps a piece can move is equal to the number of pieces on the line of the path
        * A player can capture an opponent's piece by moving into its position.
        * A piece cannot move over enemy pieces
        * A piece can move over friendly pieces
    '''
    kRows = 8
    kCols = 8
    kNumPlayers = 2
    
    # === Board Checks ===
    def is_valid_board(self):
        '''Checks if the board is valid.'''
        return self._is_valid_board_size() \
           and self._is_valid_num_players() \
           and self._is_valid_num_pieces()

    def is_valid_init_board(self, board):
        '''Checks if the board is valid for initialization.'''
        return self.is_valid_board(board) \
           and self._is_empty_corners(board) \
           and self._is_initial_player_positions(board)
    
    def _is_valid_board_size(self, board):
        return board.rows == self.kRows and board.cols == self.kCols

    def _is_valid_num_players(self, board):
        return len(board.players) == self.kNumPlayers

    def _is_valid_num_pieces(self, board):
        n1 = board.count(board.players[0])
        n2 = board.count(board.players[1])
        return n1 >= 1 and n1 < self.kCols * 2 - 4 \
           and n2 >= 1 and n2 < self.kRows * 2 - 4

    def _is_empty_corners(self, board):
        return board.peek(0, 0)      \
            == board.peek(0, -1)     \
            == board.peek(-1, 0)     \
            == board.peek(-1, -1)    \
            == Piece.EMPTY
    
    def _is_initial_player_positions(self, board):
        return board[[0, -1], 1:-1] == board.players[0] \
           and board[1:-1, [0, -1]] == board.players[1] \
           and board.count(board.players[0]) == 2 * (self.kCols - 2) \
           and board.count(board.players[1]) == 2 * (self.kRows - 2)

    # === Movement Checks and Rules ===
    def valid_directions(self):
        '''Returns the valid directions for movement + their vectors.'''
        return {
            'n': (0, -1),
            's': (0, 1),
            'e': (1, 0),
            'w': (-1, 0),
            'ne': (1, -1),
            'nw': (-1, -1),
            'se': (1, 1),
            'sw': (-1, 1),
        }

    def is_movable(self, board, position, current_player):
        '''Checks if the piece at the given position is movable.
        
        Note: Does not check if the position is valid or if the piece has moves
        '''
        piece = board.peek(position)
        return piece == current_player and piece != Piece.EMPTY

    def get_valid_steps(self, board, position, current_player):
        '''Returns the valid steps for the given position in each direction.'''
        # 1. Get the line coordinates -> get the number of piece along those coordinates
        num_pieces = {'n': 0, 's': 0, 'e': 0, 'w': 0, 'ne': 0, 'nw': 0, 'se': 0, 'sw': 0}
        for orient in 'hvda':
            line = _utils.line_coords(board.board.shape, position, orient)
            pieces = board.board[*zip(*line)]
            num = int((pieces != Piece.EMPTY).sum())
            if orient in 'hv':
                num_pieces['n'] = num
                num_pieces['s'] = num
            elif orient in 'da':
                num_pieces['ne'] = num
                num_pieces['sw'] = num
            elif orient in 'dv':
                num_pieces['nw'] = num
                num_pieces['se'] = num
            else:
                raise ValueError(f'Invalid orientation: {orient}')
        # 2. Get all line of sight coordinates
        lines_of_sight = _utils.all_line_of_sight_coords(
            board.board.shape,
            position,
            board.get_positions(~current_player),
            include_obstacles=True,
        )
        # 3. Collect the coordinates in the line of sight that are EXACTLY num_pieces away from the position
        valid_steps = set()
        for key, value in num_pieces:
            los_coords = lines_of_sight[key]
            for coord in los_coords:
                if max(abs(coord[0]-position[0]), abs(coord[1]-position[1])) == value:
                    valid_steps.add(coord)
        # 4. Remove any steps that will end up on our own piece
        valid_steps -= board.get_positions(current_player)
        return valid_steps

    # === Game Checks ===
    def is_game_over(self, board):
        '''Checks if the game is over.
        '''
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
        '''Checks if all the pieces of the given player are connected.

        Note: This uses DFS
        '''
        visited = set()
        stack = [board.get_positions(player)[0]]
        while stack:
            position = stack.pop()
            if position in visited:
                continue
            visited.add(position)
            neighbors = self._get_neighbors(board, position)
            stack.extend(neighbors)
        return len(visited) == board.count(player)
    