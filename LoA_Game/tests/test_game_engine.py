from unittest import TestCase

from linesofaction.engine import GameEngine
from linesofaction.piece import Piece
from linesofaction.board import Board

class TestGameEngineInit(TestCase):
    def test_init(self):
        # Default
        game_engine = GameEngine()
        self.assertEqual(game_engine.board.rows, 8)
        self.assertEqual(game_engine.board.cols, 8)
        # Existing board
        board = game_engine.board
        board.rows = 4
        board.cols = 4
        board._init_board()._init_pieces()
        game_engine = GameEngine(board=board)
        self.assertEqual(game_engine.board.rows, 4)
        self.assertEqual(game_engine.board.cols, 4)
    
    def test_reset(self):
        game_engine = GameEngine()
        game_engine.current_player = game_engine.board.players[1]
        game_engine.select((0, 0), player=False, reset=False)
        game_engine.winner = game_engine.board.players[0]

        game_engine.reset()
        self.assertEqual(game_engine.board.rows, 8)
        self.assertEqual(game_engine.board.cols, 8)
        self.assertEqual(game_engine.current_player, game_engine.board.players[0])
        self.assertIsNone(game_engine.winner)

class TestGameEnginePositionSelection(TestCase):
    def test_select(self):
        game_engine = GameEngine()

        # Resetting using `None` position
        game_engine._selected_position = (0, 0)
        self.assertIsNotNone(game_engine.selected['position'])
        self.assertIsNotNone(game_engine.selected['piece'])
        
        game_engine.select(None)
        self.assertIsNone(game_engine._selected_position)
        self.assertEqual(game_engine.selected, {'position': None, 'piece': None})

        # player=False, reset=False ==> Should be able to choose any position
        with self.subTest(player=False, reset=False):
            game_engine.select((0, 1), player=False, reset=False)  # Player postion
            self.assertEqual(game_engine.selected['position'], (0, 1))
            self.assertEqual(game_engine.selected['piece'], game_engine.board.players[0])

            game_engine.select((1, 0), player=False, reset=False)  # Player postion
            self.assertEqual(game_engine.selected['position'], (1, 0))
            self.assertEqual(game_engine.selected['piece'], game_engine.board.players[1])

            game_engine.select((0, 0), player=False, reset=False)  # Empty position
            self.assertEqual(game_engine.selected['position'], (0, 0))
            self.assertEqual(game_engine.selected['piece'], Piece.EMPTY)
        
        # player=False, reset=True ==> Should be able to choose any player, and reset on empty position
        with self.subTest(player=False, reset=True):
            game_engine.select((0, 1), player=False, reset=True)  # Player postion
            self.assertEqual(game_engine.selected['position'], (0, 1))
            self.assertEqual(game_engine.selected['piece'], game_engine.board.players[0])
            game_engine.select((1, 0), player=False, reset=True)  # Player postion
            self.assertEqual(game_engine.selected['position'], (1, 0))
            self.assertEqual(game_engine.selected['piece'], game_engine.board.players[1])
            game_engine.select((0, 0), player=False, reset=True)  # Empty position
            self.assertEqual(game_engine.selected['position'], None)
            self.assertEqual(game_engine.selected['piece'], None)
        
        # player=True, reset=False ==> Should only be able to choose the current player, and raise error if not allowing reset
        with self.subTest(player=True, reset=False):
            game_engine.current_player = game_engine.board.players[0]
            game_engine.select((0, 1), player=True, reset=False)
            self.assertEqual(game_engine.selected['position'], (0, 1))
            self.assertEqual(game_engine.selected['piece'], game_engine.board.players[0])
            with self.assertRaises(ValueError):
                game_engine.select((1, 0), player=True, reset=False)
            self.assertEqual(game_engine.selected['position'], (0, 1))
            self.assertEqual(game_engine.selected['piece'], game_engine.board.players[0])
            
            game_engine.current_player = game_engine.board.players[1]
            game_engine.select((1, 0), player=True, reset=False)
            self.assertEqual(game_engine.selected['position'], (1, 0))
            self.assertEqual(game_engine.selected['piece'], game_engine.board.players[1])
            with self.assertRaises(ValueError):
                game_engine.select((0, 1), player=True, reset=False)
            self.assertEqual(game_engine.selected['position'], (1, 0))
            self.assertEqual(game_engine.selected['piece'], game_engine.board.players[1])

        # player=True, reset=True ==> Should only be able to choose the current player, and reset on any other position
        with self.subTest(player=True, reset=True):
            game_engine.current_player = game_engine.board.players[0]

            game_engine._selected_position = (0, 3)
            game_engine.select((0, 1), player=True, reset=True)
            self.assertEqual(game_engine.selected['position'], (0, 1))
            self.assertEqual(game_engine.selected['piece'], game_engine.board.players[0])

            game_engine.select((1, 0), player=True, reset=True)
            self.assertEqual(game_engine.selected['position'], None)
            self.assertEqual(game_engine.selected['piece'], None)

            game_engine._selected_position = (0, 1)
            game_engine.select((0, 0), player=True, reset=True)
            self.assertEqual(game_engine.selected['position'], None)
            self.assertEqual(game_engine.selected['piece'], None)
    
    def test_get_positions(self):
        board = Board(rows=4, cols=4)
        game_engine = GameEngine(board=board)

        # Player 1 positions
        expected = sorted([(0, 1), (0, 2), (3, 1), (3, 2)])
        self.assertEqual(game_engine.get_positions(), expected)

        # Player 2 positions
        game_engine.current_player = game_engine.board.players[1]
        expected = sorted([(1, 0), (2, 0), (1, 3), (2, 3)])
        self.assertEqual(game_engine.get_positions(), expected)

        # Empty board
        board._init_board()
        self.assertEqual(game_engine.get_positions(), [])

class TestGameEngineGamePlay(TestCase):
    def setUp(self):
        board = Board(rows=4, cols=4)
        self.game_engine = GameEngine(board=board)

    def test_move_invalid_selection(self):
        self.game_engine.select(None)
        with self.assertRaises(ValueError, msg='Should not be able to move without selecting a piece'):
            self.game_engine.move((0, 1))
        
        self.game_engine.select((0, 0), player=False, reset=False)
        with self.assertRaises(ValueError, msg='Should not be able to move unowned piece'):
            self.game_engine.move((0, 1))
        
        self.game_engine.select((1, 0), player=False, reset=False)
        with self.assertRaises(ValueError, msg='Should not be able to move unowned piece'):
            self.game_engine.move((0, 1))

    def test_move_force(self):
        self.game_engine.select((1, 0), player=False, reset=False)  # Force-select player 2
        self.game_engine.move((0, 1), force=True)  # Force move to player 1
        self.assertEqual(self.game_engine.board.peek(1, 0), Piece.EMPTY)
        self.assertEqual(self.game_engine.board.peek(0, 1), self.game_engine.board.players[1])

        # Moving to the owned piece
        self.game_engine.select((-1, 1), player=True, reset=False)  # Force-select player 1
        self.game_engine.move((-1, 2), force=True)  # Force move to player 1
        self.assertEqual(self.game_engine.board.peek(-1, 1), Piece.EMPTY)
        self.assertEqual(self.game_engine.board.peek(-1, 2), self.game_engine.current_player)

        # game_engine.current_player = game_engine.board.players[1]
        # game_engine.selected = (1, 0)
        # game_engine.move((2, 0))
        # self.assertEqual(game_engine.board.peek(1, 0), Piece.EMPTY)
        # self.assertEqual(game_engine.board.peek(2, 0), game_engine.board.players[1])

# class TestGameEngineRules(TestCase):
#     def setUp(self):
#         board = Board(rows=8, cols=8)
#         board.board = np.array()
#         self.game_engine = GameEngine(board=board)



    # def test_lines_of_sight(self):