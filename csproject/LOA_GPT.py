import graphics as g
from enum import StrEnum

GRID_SIZE = 8
CELL_SIZE = 60
MARGIN = 100


class Piece(StrEnum):
    EMPTY = 'empty'
    RED = 'red'
    BLUE = 'blue'



def initialize_board():
    board = [['empty' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for col in range(1, 7):
        board[0][col] = 'blue'
        board[7][col] = 'blue'
    for row in range(1, 7):
        board[row][0] = 'red'
        board[row][7] = 'red'
    return board

def fill_cell_background(win, board):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x1 = MARGIN + col * CELL_SIZE
            y1 = MARGIN + (GRID_SIZE - row - 1) * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            fill_color = 'red' if board[row][col] == 'red' else 'blue' if board[row][col] == 'blue' else 'antiquewhite'
            rect = g.Rectangle(g.Point(x1, y1), g.Point(x2, y2))
            rect.setFill(fill_color)
            rect.setWidth(0)
            rect.draw(win)

def draw_grid(win):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x1 = MARGIN + col * CELL_SIZE
            y1 = MARGIN + (GRID_SIZE - row - 1) * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            rect = g.Rectangle(g.Point(x1, y1), g.Point(x2, y2))
            rect.setWidth(2)
            rect.draw(win)

def main():
    board = initialize_board()
    win = g.GraphWin("Lines of Action", 680, 680)
    win.setBackground("white")

    fill_cell_background(win, board)
    draw_grid(win)

    current_player = 'red'
    while True:
        # Simplified turn handling logic.
        print(f"{current_player.capitalize()}'s turn.")
        # Logic for handling moves, checking win, etc.

        # Switch turns.
        current_player = 'blue' if current_player == 'red' else 'red'

if __name__ == "__main__":
    main()