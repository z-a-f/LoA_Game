from unittest import TestCase

from linesofaction.direction import Direction

class TestDirection(TestCase):
    def test_str2value(self):
        self.assertEqual(Direction.str2value('N'), Direction.N.value)
        self.assertEqual(Direction.str2value('n'), Direction.N.value)
        self.assertEqual(Direction.str2value('nW'), Direction.NW.value)
        self.assertEqual(Direction.str2value('NORTH'), Direction.N.value)
        self.assertEqual(Direction.str2value('NORTHWEST'), Direction.NW.value)
        self.assertEqual(Direction.str2value('NORTH WEST'), Direction.NW.value)
        self.assertEqual(Direction.str2value('NORTH_WEST'), Direction.NW.value)
    
    def test_string(self):
        self.assertEqual(Direction([1, 1]), Direction('SE'))
        self.assertEqual(Direction([1, 1]), Direction('SOUTH_EAST'))
    
    def test_non_unit(self):
        self.assertEqual(Direction([2, 2]), Direction([1, 1]))
        self.assertEqual(Direction([2, 0]), Direction([1, 0]))
        self.assertEqual(Direction([-10, -0.1]), Direction([-1, -1]))
