from board import Board as b
import pytest

def test_empty_matrix():
    matrix = []
    result = b.find_connected_sequence(matrix)
    assert result == []

def test_matrix_with_only_zeros():
    matrix = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    result = b.find_connected_sequence(matrix)
    assert result == []

def test_single_value_matrix():
    matrix = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]
    result = b.find_connected_sequence(matrix)
    assert result == [
        [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    ]

def test_mixed_matrix():
    matrix = [
        [1, 1, 0, 2],
        [1, 1, 0, 2],
        [0, 1, 2, 2],
        [0, 1, 1, 2]
    ]
    result = b.find_connected_sequence(matrix)
    expected = [
        [(0, 0), (0, 1), (1, 0), (1, 1)],  # Connected sequence of 1s
        [(0, 3), (1, 3), (2, 2), (2, 3), (3, 3)],  # Connected sequence of 2s
        [(2, 1)],  # Single 1
        [(3, 1), (3, 2)]  # Connected sequence of 1s
    ]
    assert result == expected

def test_single_element_matrix():
    matrix = [
        [1]
    ]
    result = b.find_connected_sequence(matrix)
    assert result == [
        [(0, 0)]  # Single element 1
    ]

    matrix = [
        [2]
    ]
    result = b.find_connected_sequence(matrix)
    assert result == [
        [(0, 0)]  # Single element 2
    ]

def test_edge_case_with_diagonal_connection():
    matrix = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]
    result = b.find_connected_sequence(matrix)
    # All 1s are diagonally connected
    assert result == [
        [(0, 0), (1, 1), (2, 2)]  # Diagonal sequence of 1s
    ]

def test_mixed_zeroes_and_ones():
    matrix = [
        [1, 0, 1],
        [1, 1, 1],
        [0, 1, 0]
    ]
    result = b.find_connected_sequence(matrix)
    # We have two connected regions of 1s: one at top-left and one forming a 'T' in the center
    expected = [
        [(0, 0), (1, 0)],  # First connected sequence of 1s
        [(0, 2)],  # Single 1
        [(1, 1), (1, 2), (2, 1)]  # Connected sequence of 1s forming a 'T'
    ]
    assert result == expected