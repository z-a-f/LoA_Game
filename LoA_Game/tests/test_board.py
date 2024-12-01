from unittest import TestCase
from itertools import product

from linesofaction.board import Board
from linesofaction.piece import Piece

class TestBoardInitialization(TestCase):
    def test_init_board_shape(self):
        # Valid rows
        rows_under_test = [8, 10]
        cols_under_test = [8, 10]
        for rows, cols in product(rows_under_test, cols_under_test):
            with self.subTest(rows=rows, cols=cols):
                board = Board(rows=rows, cols=cols)
                self.assertEqual(board.rows, rows)
                self.assertEqual(board.cols, cols)
                self.assertEqual(board.board.shape, (rows, cols))
        
        # Invalid rows
        rows_under_test = range(3)
        cols_under_test = range(3)
        for rows, cols in product(rows_under_test, cols_under_test):
            with self.subTest(rows=rows, cols=cols), self.assertRaises(ValueError):
                board = Board(rows=rows, cols=cols)
    
    def test_init_board_dtype(self):
        board = Board(rows=4, cols=4)
        self.assertEqual(board.board.dtype, int)
    
    def test_init_board_empty_values(self):
        board = Board(rows=4, cols=4)
        board._init_board()  # This reinitializes an empty board
        self.assertTrue((board.board == Piece.EMPTY).all())
    
    def test_init_board_player_positions(self):
        board = Board(rows=4, cols=4)
        board._init_pieces()
        # Player 1 should occupy the first and last rows
        self.assertTrue((board.board[[0, -1], 1:-1] == board.players[0]).all())
        # Player 2 should occupy the first and last co9lumns
        self.assertTrue((board.board[1:-1, [0, -1]] == board.players[1]).all())
    
    def test_repr(self):
        board = Board(rows=4, cols=4)
        self.assertEqual(str(board), '  | A B C D\n--+--------\n1 | . b b .\n2 | r . . r\n3 | r . . r\n4 | . b b .')


class TestBoardMethods(TestCase):    
    def test_count(self):
        board = Board(rows=7, cols=9)
        board._init_board()  # Initially should be all empty
        self.assertEqual(board.count(Piece.EMPTY), board.rows * board.cols)
        self.assertEqual(board.count(board.players[0]), 0)
        self.assertEqual(board.count(board.players[1]), 0)
        board._init_pieces()  # Now we have pieces on the board
        self.assertEqual(board.count(Piece.EMPTY), (board.rows - 2) * (board.cols - 2) + 4)
        self.assertEqual(board.count(board.players[0]), 2 * (board.cols - 2))
        self.assertEqual(board.count(board.players[1]), 2 * (board.rows - 2))

        # Check that the count is correct after replacing pieces
        board.replace((0, 1), board.players[1])
        self.assertEqual(board.count(board.players[0]), 2 * (board.cols - 2) - 1, f'\n{board}')
        self.assertEqual(board.count(board.players[1]), 2 * (board.rows - 2) + 1, f'\n{board}')

        # Check that the count is correct after popping pieces
        board.pop((0, 1))
        self.assertEqual(board.count(board.players[1]), 2 * (board.rows - 2), f'\n{board}')
    
    def test_get_positions(self):
        board = Board(rows=4, cols=4)
        player1_positions = set(product([0, 3], range(1, 3)))
        player2_positions = set(product(range(1, 3), [0, 3]))
        empty_positions = (set(product(range(4), range(4))) - player1_positions - player2_positions)
        
        self.assertEqual(board.get_positions(board.players[0]), sorted(player1_positions))
        self.assertEqual(board.get_positions(board.players[1]), sorted(player2_positions))
        self.assertEqual(board.get_positions(Piece.EMPTY), sorted(empty_positions))

class TestBoardPieceManipulation(TestCase):
    def test_peek(self):
        board = Board(rows=4, cols=4)
        player1_positions = list(product([0, 3], range(1, 3)))
        player2_positions = list(product(range(1, 3), [0, 3]))

        for position in player1_positions:
            with self.subTest(position=position, player=board.players[0]):
                self.assertEqual(board.peek(*position), board.players[0])
                self.assertEqual(board.board[position], board.players[0])
        for position in player2_positions:
            with self.subTest(position=position, player=board.players[1]):
                self.assertEqual(board.peek(*position), board.players[1])
                self.assertEqual(board.board[position], board.players[1])
        
        # Nothing should have changed
        for row, col in product(range(board.rows), range(board.cols)):
            with self.subTest(row=row, col=col):
                if (row, col) in player1_positions:
                    self.assertEqual(board.board[row, col], board.players[0])
                elif (row, col) in player2_positions:
                    self.assertEqual(board.board[row, col], board.players[1])
                else:
                    self.assertEqual(board.board[row, col], Piece.EMPTY)
        
    def test_pop(self):
        board = Board(rows=4, cols=4)
        player1_positions = product([0, 3], range(1, 3))
        player2_positions = product(range(1, 3), [0, 3])

        for position in player1_positions:
            with self.subTest(position=position, player=board.players[0]):
                self.assertEqual(board.pop(position), board.players[0])
                self.assertEqual(board.board[position], Piece.EMPTY)
        for position in player2_positions:
            with self.subTest(position=position, player=board.players[1]):
                self.assertEqual(board.pop(position), board.players[1])
                self.assertEqual(board.board[position], Piece.EMPTY)
        
        # Everything should be empty now
        for row, col in product(range(4), range(4)):
            self.assertEqual(board.pop((row, col)), Piece.EMPTY)
    
    def test_place(self):
        board = Board(rows=4, cols=4)
        board._init_board()  # This reinitializes an empty board
        player1_positions = list(product([0, 3], range(1, 3)))
        player2_positions = list(product(range(1, 3), [0, 3]))

        for position in player1_positions:
            with self.subTest(position=position, player=board.players[0]):
                board.place(position, board.players[0])
                self.assertEqual(board.board[position], board.players[0])
        
        for position in player2_positions:
            with self.subTest(position=position, player=board.players[1]):
                board.place(position, board.players[1])
                self.assertEqual(board.board[position], board.players[1])
        
        # Check that we raise an error if we try to place a piece on a non-empty square
        for position in player1_positions + player2_positions:
            with self.subTest(position=position), self.assertRaises(ValueError):
                    board.place(position, board.players[0])
        
        # Check that the rest of the board is not affected
        for row, col in product(range(4), range(4)):
            with self.subTest(row=row, col=col):
                if (row, col) in player1_positions:
                    self.assertEqual(board.board[row, col], board.players[0])
                elif (row, col) in player2_positions:
                    self.assertEqual(board.board[row, col], board.players[1])
                else:
                    self.assertEqual(board.board[row, col], Piece.EMPTY)
