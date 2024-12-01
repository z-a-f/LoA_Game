
from unittest import TestCase
from itertools import product
import numpy as np

from linesofaction._utils import line_mask, line_of_sight_mask, all_lines_of_sight_mask

class TestStrEnumImport(TestCase):
    def test_str_enum_import(self):
        try:
            from linesofaction._utils import StrEnum
        except ImportError:
            self.fail('StrEnum import failed')


class TestMaskLine(TestCase):
    def test_rows_cols(self):
        shapes = [(4, 4), (4, 5), (5, 4), (5, 5)]
        pivots = [(0, 0), (0, 1), (1, 1), (2, 2), (-1, -1)]
        orientations = ['horizontal', 'vertical']
        for shape, pivot, orientation in product(shapes, pivots, orientations):
            with self.subTest(shape=shape, pivot=pivot, orientation=orientation):
                mask = line_mask(shape, pivot, orientation)
                self.assertEqual(mask.shape, shape)
                if orientation == 'horizontal':
                    self.assertTrue(np.all(mask[pivot[0], :]))
                if orientation == 'vertical':
                    self.assertTrue(np.all(mask[:, pivot[1]]))
                self.assertEqual(np.sum(mask), shape[0] if orientation == 'vertical' else shape[1])
    
    def test_diagonal(self):
        cases = {
            ((3, 4), (0, 0), 'diagonal'): [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0]],
            ((3, 4), (0, 0), 'antidiagonal'): [
                [1, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]],
            ((3, 4), (1, 2), 'diagonal'): [
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]],
            ((3, 4), (1, 2), 'antidiagonal'): [
                [0, 0, 0, 1],
                [0, 0, 1, 0],
                [0, 1, 0, 0]],
            ((3, 4), (-2, -1), 'diagonal'): [
                [0, 0, 1, 0],
                [0, 0, 0, 1],
                [0, 0, 0, 0]],
            ((3, 4), (-1, -2), 'antidiagonal'): [
                [0, 0, 0, 0],
                [0, 0, 0, 1],
                [0, 0, 1, 0]],
        }
        for (shape, pivot, orientation), expected in cases.items():
            expected = np.array(expected, dtype=bool)
            with self.subTest(shape=shape, pivot=pivot, orientation=orientation):
                mask = line_mask(shape, pivot, orientation)
                self.assertTrue((mask==expected).all(), f'Expected({pivot}):\n{expected}\nGot:\n{mask}')

class TestLineOfSight(TestCase):
    def test_lines_of_sight_mask_no_obst(self):
        obstructions = np.array([
            [0, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0],
        ], dtype=bool)
        orientation_legend = {'obstruction': 1, 'pivot': 2, 'h': 3, 'v': 4, 'd': 5, 'a': 6}
        expected = {  # pivot -> line of sight; 1=obstruction, 2=pivot, 3=horizontal, 4=vertical, 5=diagonal, 6=antidiagonal
            (0, 0): [[2, 3, 3, 3],
                     [4, 0, 0, 0],
                     [4, 0, 0, 0]],
            (0, 1): [[3, 2, 3, 3],
                     [6, 0, 5, 0],
                     [0, 0, 0, 5]],
            (1, 1): [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]],
            (2, 2): [[0, 0, 4, 0],
                     [0, 0, 4, 6],
                     [3, 3, 2, 3]],
            (-1, -1):[[0, 5, 0, 4],
                      [0, 0, 5, 4],
                      [3, 3, 3, 2]],
        }

        for pivot in expected.keys():
            for orientation in 'hvda':
                with self.subTest(pivot=pivot, orientation=orientation):
                    expected_mask = np.logical_or(
                        np.array(expected[pivot]) == orientation_legend[orientation],
                        np.array(expected[pivot]) == orientation_legend['pivot'],
                        np.array(expected[pivot]) == orientation_legend['obstruction'],
                    )
                    mask = line_of_sight_mask(obstructions, pivot, orientation, include_obstacles=False)
                    self.assertTrue(np.all(mask==expected_mask), f'Expected({pivot}):\n{expected_mask}\nGot:\n{mask}')
            
            with self.subTest(pivot=pivot, orientation='all'):
                expected_mask = np.array(expected[pivot], dtype=bool)
                mask = all_lines_of_sight_mask(obstructions, pivot, include_obstacles=False)
                self.assertTrue(np.all(mask==expected_mask), f'Expected({pivot}):\n{expected_mask}\nGot:\n{mask}')
    
    def test_lines_of_sight_mask_with_obst(self):
        obstructions = np.array([
            [0, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0],
        ], dtype=bool)
        orientation_legend = {'obstruction': 1, 'pivot': 2, 'h': 3, 'v': 4, 'd': 5, 'a': 6}
        expected = {  # pivot -> line of sight; 1=obstruction, 2=pivot, 3=horizontal, 4=vertical, 5=diagonal, 6=antidiagonal
            (0, 0): [[2, 3, 3, 3],
                     [4, 5, 0, 0],
                     [4, 0, 0, 0]],
            (0, 1): [[3, 2, 3, 3],
                     [6, 4, 5, 0],
                     [0, 0, 0, 5]],
            (1, 1): [[0, 0, 0, 0],
                     [0, 2, 0, 0],
                     [0, 0, 0, 0]],
            (2, 2): [[0, 0, 4, 0],
                     [0, 5, 4, 6],
                     [3, 3, 2, 3]],
            (-1, -1):[[0, 5, 0, 4],
                      [0, 0, 5, 4],
                      [3, 3, 3, 2]],
        }

        for pivot in expected.keys():
            for orientation in 'hvda':
                with self.subTest(pivot=pivot, orientation=orientation):
                    expected_mask = np.logical_or(
                        np.array(expected[pivot]) == orientation_legend[orientation],
                        np.array(expected[pivot]) == orientation_legend['pivot'],
                    )
                    mask = line_of_sight_mask(obstructions, pivot, orientation, include_obstacles=True)
                    self.assertTrue(np.all(mask==expected_mask), f'Expected({pivot}):\n{expected_mask}\nGot:\n{mask}')
            with self.subTest(pivot=pivot, orientation='all'):
                expected_mask = np.array(expected[pivot], dtype=bool)

                mask = all_lines_of_sight_mask(obstructions, pivot, include_obstacles=True)
                self.assertTrue(np.all(mask==expected_mask), f'Expected({pivot}):\n{expected_mask}\nGot:\n{mask}')
