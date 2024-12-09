#!/usr/bin/env python3
import sys
import string

from linesofaction import LinesOfActionGame
from linesofaction import _utils
from linesofaction.piece import Piece
from linesofaction.rules import GameEndState

def parse_position(pos_str):
    '''Parses a position like "A1" into (row, col) indices.
    
    Columns are letters (A,B,C,...), rows are numbers starting from 1.
    Board indexing: top-left is A1, top row is 1, leftmost column is A.
    Internally, rows and columns are zero-based indexed.
    '''
    pos_str = pos_str.strip().upper()
    if len(pos_str) < 2:
        raise ValueError('Position too short. Must be like A1.')

    # Extract the column letter(s) and row number
    col_part = ''.join([ch for ch in pos_str if ch.isalpha()])
    row_part = ''.join([ch for ch in pos_str if ch.isdigit()])

    if not col_part or not row_part:
        raise ValueError('Invalid position format. Example: A1, C3.')

    col = 0
    # Handle multiple letters for columns if board larger than 26 columns
    # For a standard 8x8 board, this is not necessary, but let's be general
    for ch in col_part:
        col = col * 26 + (ord(ch) - ord('A'))

    row = int(row_part) - 1
    return (row, col)


def position_to_str(row, col):
    '''Converts (row, col) to a standard chess-like notation: A1, B3, etc.'''
    # For columns beyond 'Z', we can use a double-letter system if needed
    # For standard LOA (8x8), only single-letter is required
    letters = []
    base = col
    while True:
        letters.append(chr(base % 26 + ord('A')))
        base = base // 26 - 1
        if base < 0:
            break
    col_str = ''.join(reversed(letters))
    return f'{col_str}{row+1}'


def print_board(engine):
    '''Prints the board state.'''
    print(engine)
    print(f"Current Player: {engine.current_player.name.capitalize()}\n")


def main():
    # Initialize the game
    engine = LinesOfActionGame()
    rules = engine.rules  # Just a reference if needed
    print("Welcome to Lines of Action!")
    print("Players: Black (b) and Red (r)")
    print("To move, first select a piece you own, then select a destination.")
    print("Positions are specified like A1, B3, etc.\n")

    # Main game loop
    while True:
        print_board(engine)

        # Check if game is already over
        if engine.winner is not None:
            if engine.winner == 'TIE':
                print("The game ended in a tie!")
            else:
                print(f"The winner is: {engine.winner.name.capitalize()}!")
            break

        # Prompt to select a piece
        while True:
            try:
                piece_pos_str = input(f"({engine.current_player.name.capitalize()}) Select a piece: ")
                piece_pos = parse_position(piece_pos_str)
                # Try selecting this piece
                engine.select(piece_pos, player=True, reset=True)
                if engine.selected['position'] is None:
                    print("Invalid selection. You must select one of your own pieces.")
                    continue
                # Selected a piece successfully, break
                break
            except ValueError as e:
                print(e)
                continue

        # Show valid moves
        try:
            valid_moves = engine.get_valid_moves()
        except ValueError:
            valid_moves = set()  # No valid moves
        if not valid_moves:
            print("No valid moves for this piece. Deselecting.")
            engine.select(None)  # Deselect
            continue

        print("Valid moves:")
        for mv in valid_moves:
            print(position_to_str(*mv), end=' ')
        print('\n')

        # Prompt for a move
        while True:
            try:
                move_pos_str = input(f"({engine.current_player.name.capitalize()}) Move to: ")
                move_pos = parse_position(move_pos_str)
                engine.move(move_pos)  # Will raise if invalid
                break
            except ValueError as e:
                print(e)
                print("Try another position or type Ctrl+C to exit.")
                continue

        # After a move, engine checks game state and switches player automatically.
        # Loop continues until game over.


if __name__ == '__main__':
    main()
