# Lines of Action (LoA) CLI Game

To run the game:

```shell
python ./LoA_CLI.py
```

which will present you with

```console
Welcome to Lines of Action!
Players: Black (b) and Red (r)
To move, first select a piece you own, then select a destination.
Positions are specified like A1, B3, etc.

  | A B C D E F G H
--+----------------
1 | . b b b b b b .
2 | r . . . . . . r
3 | r . . . . . . r
4 | r . . . . . . r
5 | r . . . . . . r
6 | r . . . . . . r
7 | r . . . . . . r
8 | . b b b b b b .
Current Player: Black

(Black) Select a piece: 
```

# Lines of Action (LoA) Python Package

The **Lines of Action** package provides classes and utilities to implement and play the [Lines of Action](https://en.wikipedia.org/wiki/Lines_of_Action) board game. It includes a `Board` representation, game `Engine` for running turns and moves, `Rules` to validate moves and endgame conditions, and `Piece` types. Additionally, it has utility functions for line-of-sight computation, directions, and printing.

## Table of Contents
- [Examples](#examples)
- [Package Structure](#package-structure)
- [Modules](#modules)
  - [linesofaction.engine](#linesofactionengine)
  - [linesofaction.board](#linesofactionboard)
  - [linesofaction.piece](#linesofactionpiece)
  - [linesofaction.rules](#linesofactionrules)
  - [linesofaction.direction](#linesofactiondirection)
  - [linesofaction._utils](#linesofaction_utils)
- [Classes and Methods](#classes-and-methods)
  - [GameEngine](#gameengine-class)
  - [Board](#board-class)
  - [Piece](#piece-class)
  - [GameRules](#gamerules-class)
  - [Direction](#direction-enum)

--

## Examples

**Initializing a Game:**
```python
from linesofaction import LinesOfActionGame

engine = LinesOfActionGame()  # 8x8 board by default
print(engine)  # Prints the board

positions = engine.get_positions()
print("Current Player Pieces:", positions)
```

**Selecting and Moving a Piece:**
```python
# Select a piece owned by the current player
engine.select((0,1))  
valid_moves = engine.get_valid_moves()
print("Valid moves:", valid_moves)

# Move to a valid position
if valid_moves:
    move_to = valid_moves.pop()  
    engine.move(move_to)
    print(engine)
```

**Checking Game End:**
```python
if engine.winner is not None:
    print("Game Over! Winner:", engine.winner)
```

## Package Structure

```
linesofaction/
    __init__.py            # Imports GameEngine as LinesOfActionGame
    engine.py              # The GameEngine class and logic to run the game
    board.py               # The Board class and logic for piece placement, querying, etc.
    piece.py               # The Piece enum representing empty, red, and black pieces
    rules.py               # The GameRules class enforcing LOA rules and endgame conditions
    direction.py           # The Direction enum for handling directional moves
    _utils.py              # Internal utility functions for line-of-sight, printing, etc.
```

## Modules

### linesofaction.engine
Contains the `GameEngine` class which orchestrates gameplay:
- Initializing a `Board`
- Handling player turns
- Selecting pieces
- Making moves and applying `GameRules`
- Determining game outcome

### linesofaction.board
Defines the `Board` class representing the LOA board:
- Creation of NxN boards
- Initial piece placement
- Querying and modifying piece positions (peek, pop, place)
- Counting pieces and retrieving their positions

### linesofaction.piece
Defines the `Piece` enum with:
- `EMPTY`, `RED`, `BLACK`
- Methods to get opposite colors, chars, etc.

### linesofaction.rules
Implements the `GameRules` class:
- Validates board states
- Determines valid moves
- Checks connectivity for endgame conditions
- Handles piece line-of-sight and movement constraints

### linesofaction.direction
Contains `Direction` enum:
- N, S, E, W, NE, NW, SE, SW directions as vectors
- Methods for combining and inverting directions

### linesofaction._utils
Utility functions:
- Line-of-sight computations (`line_coords`, `all_line_of_sight_coords`)
- Board printing and formatting (`to_lines`, `print_mask`)
- Orientation conversions and masks for lines

## Classes and Methods

### GameEngine Class
**Location:** `linesofaction/engine.py`

**Purpose:** Manages the state of the game, the current player, and executes moves in accordance with the rules.

**Key Methods:**
- `__init__(board=None)`: Initialize the engine with a given or new `Board`.
- `reset()`: Reset the game to the initial state.
- `select(position=None, player=True, reset=True)`: Select or deselect a piece.
- `get_positions()`: Returns positions of the current player's pieces.
- `get_valid_moves()`: Returns valid moves for the currently selected piece.
- `move(position, force=False)`: Move the selected piece to the given position if valid.
- `next_turn()`: Switch the current player if the game continues.
- `__repr__()`: Returns a string representation of the current board state.

### Board Class
**Location:** `linesofaction/board.py`

**Purpose:** Represents the LOA board and provides methods to query and manipulate pieces.

**Key Methods:**
- `__init__(rows=8, cols=8)`: Create an empty board of given size.
- `count(piece)`: Count how many pieces of a type are on the board.
- `get_positions(piece)`: Get positions of a given piece as a list of (row, col).
- `peek(position)`: Return the piece at a given position without modifying the board.
- `pop(position)`: Remove and return the piece at `position`.
- `place(position, piece)`: Place a piece on an empty square.
- `replace(position, piece)`: Replace whatever is at position with given piece.
- `is_empty(position)`: Check if a position is empty.
- `is_player(position, player=None)`: Check if position is occupied by a given player.

### Piece Class
**Location:** `linesofaction/piece.py`

**Purpose:** Enum for piece types:
- `EMPTY`
- `RED`
- `BLACK`

**Key Methods:**
- `color()`: Returns color name as string.
- `opposite()`: Returns the opposite piece color.
- `char(offset=None)`: Returns a character representation of the piece.

### GameRules Class
**Location:** `linesofaction/rules.py`

**Purpose:** Enforces LOA rules, including valid moves and endgame checks.

**Key Methods:**
- `is_valid_board(board)`: Validate if the board configuration is correct.
- `is_valid_init_board(board)`: Check if it's a proper initial LOA board.
- `is_movable(board, position, current_player)`: Check if a piece at `position` can move.
- `get_valid_steps(board, position, current_player)`: Get valid moves for a piece.
- `is_game_over(board)`: Determine if the game has ended (win/tie/continue).

### Direction Enum
**Location:** `linesofaction/direction.py`

**Purpose:** Enum representing directions as vectors.

**Directions:**
- N, S, E, W, NE, NW, SE, SW

**Key Operators:**
- `__invert__()`: Invert direction
- `__add__()`: Combine directions
