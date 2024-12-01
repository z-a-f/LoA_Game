from unittest import TestCase

from linesofaction.piece import Piece


class TestPiece(TestCase):
    def test_unique_values(self):
        self.assertEqual(len(Piece), 3)
        self.assertEqual(len(set(Piece)), 3)
    
    def test_has_empty(self):
        # 0 should always represent empty
        self.assertEqual(Piece(0), Piece.EMPTY)
    
    def test_color(self):
        self.assertEqual(Piece.EMPTY.color(), 'white')
        self.assertEqual(Piece.RED.color(), 'red')
        self.assertEqual(Piece.BLACK.color(), 'black')
    
    def test_opposite(self):
        self.assertEqual(Piece.EMPTY.opposite(), Piece.EMPTY)
        self.assertEqual(Piece.RED.opposite(), Piece.BLACK)
        self.assertEqual(Piece.BLACK.opposite(), Piece.RED)

    def test_char(self):
        self.assertEqual(Piece.EMPTY.char(), '.')
        self.assertEqual(Piece.RED.char(), 'r')
        self.assertEqual(Piece.BLACK.char(), 'b')

