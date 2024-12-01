from graphics import *

GRID_SIZE = 8  # 8x8 grid
CELL_SIZE = 60  # Size of each square cell
MARGIN = 100  # Margin from the edges of the window

class Cell:
    def __init__(self, row, col, occupancy='empty'):
        self.row = row
        self.col = col
        self.occupancy = occupancy  # 'empty', 'red', or 'blue'
        self.rect = None
        self.highlight_rect = None

    def draw(self, win):
        x1 = MARGIN + self.col * CELL_SIZE
        y1 = MARGIN + (GRID_SIZE - self.row - 1) * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE

        # Determine fill color
        if self.occupancy == 'red':
            fill_color = 'red'
        elif self.occupancy == 'blue':
            fill_color = 'royalblue'
        else:
            fill_color = 'antiquewhite'

        # Draw the rectangle
        self.rect = Rectangle(Point(x1, y1), Point(x2, y2))
        self.rect.setFill(fill_color)
        self.rect.setWidth(2)
        self.rect.draw(win)

    def update(self, win):
        if self.rect:
            # Update fill color
            if self.occupancy == 'red':
                fill_color = 'red'
            elif self.occupancy == 'blue':
                fill_color = 'royalblue'
            else:
                fill_color = 'antiquewhite'
            self.rect.setFill(fill_color)
        else:
            self.draw(win)

    def highlight(self, win, color='yellow'):
        if self.highlight_rect:
            self.highlight_rect.undraw()
        x1 = MARGIN + self.col * CELL_SIZE
        y1 = MARGIN + (GRID_SIZE - self.row - 1) * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE

        outline_padding = 2
        x1 += outline_padding
        y1 += outline_padding
        x2 -= outline_padding
        y2 -= outline_padding

        self.highlight_rect = Rectangle(Point(x1, y1), Point(x2, y2))
        self.highlight_rect.setOutline(color)
        self.highlight_rect.setWidth(5)
        self.highlight_rect.draw(win)

    def clear_highlight(self):
        if self.highlight_rect:
            self.highlight_rect.undraw()
            self.highlight_rect = None

class Board:
    def __init__(self, win):
        self.win = win
        self.grid = [[Cell(row, col) for col in range(GRID_SIZE)]
                     for row in range(GRID_SIZE)]
        self.initialize_board()
        self.draw_board()

    def initialize_board(self):
        # Set up blue pieces
        for col in range(1, 7):
            self.grid[0][col].occupancy = 'blue'  # Top row
            self.grid[7][col].occupancy = 'blue'  # Bottom row

        # Set up red pieces
        for row in range(1, 7):
            self.grid[row][0].occupancy = 'red'  # Left column
            self.grid[row][7].occupancy = 'red'  # Right column

    def draw_board(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self.grid[row][col].draw(self.win)
        self.draw_labels()

    def draw_labels(self):
        # Draw column labels (A-H) at top and bottom
        for col in range(GRID_SIZE):
            x_label = MARGIN + col * CELL_SIZE + CELL_SIZE / 2
            # Top label
            y_label_top = MARGIN - 20
            col_label_top = Text(Point(x_label, y_label_top),
                                 chr(65 + col))
            col_label_top.setSize(12)
            col_label_top.setStyle('bold')
            col_label_top.draw(self.win)
            # Bottom label
            y_label_bottom = MARGIN + GRID_SIZE * CELL_SIZE + 20
            col_label_bottom = Text(Point(x_label, y_label_bottom),
                                    chr(65 + col))
            col_label_bottom.setSize(12)
            col_label_bottom.setStyle('bold')
            col_label_bottom.draw(self.win)
        # Draw row labels (1-8) on left and right
        for row in range(GRID_SIZE):
            y_label = MARGIN + (GRID_SIZE - row - 1) * CELL_SIZE + \
                      CELL_SIZE / 2
            # Left label
            x_label_left = MARGIN - 20
            row_label_left = Text(Point(x_label_left, y_label),
                                  str(GRID_SIZE - row))
            row_label_left.setSize(12)
            row_label_left.setStyle('bold')
            row_label_left.draw(self.win)
            # Right label
            x_label_right = MARGIN + GRID_SIZE * CELL_SIZE + 20
            row_label_right = Text(Point(x_label_right, y_label),
                                   str(GRID_SIZE - row))
            row_label_right.setSize(12)
            row_label_right.setStyle('bold')
            row_label_right.draw(self.win)

    def get_cell(self, row, col):
        return self.grid[row][col]

    def move_piece(self, start_row, start_col, end_row, end_col, player):
        self.grid[end_row][end_col].occupancy = player
        self.grid[start_row][start_col].occupancy = 'empty'
        # Update cells
        self.grid[start_row][start_col].update(self.win)
        self.grid[end_row][end_col].update(self.win)

    def highlight_cell(self, row, col, color='yellow'):
        self.grid[row][col].highlight(self.win, color)

    def highlight_possible_moves(self, possible_moves):
        for move_row, move_col in possible_moves:
            self.grid[move_row][move_col].highlight(self.win, 'green')

    def clear_highlights(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self.grid[row][col].clear_highlight()

    def get_possible_moves(self, row, col, player_color):
        possible_moves = []
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (-1, -1), (1, -1), (-1, 1)
        ]
        for direction in directions:
            row_delta, col_delta = direction
            occupied_cells = []
            # Check forward
            check_row, check_col = row, col
            while 0 <= check_row < GRID_SIZE and \
                  0 <= check_col < GRID_SIZE:
                if self.grid[check_row][check_col].occupancy != 'empty':
                    occupied_cells.append((check_row, check_col))
                check_row += row_delta
                check_col += col_delta
            # Check backward
            check_row, check_col = row, col
            while 0 <= check_row < GRID_SIZE and \
                  0 <= check_col < GRID_SIZE:
                if self.grid[check_row][check_col].occupancy != 'empty':
                    occupied_cells.append((check_row, check_col))
                check_row -= row_delta
                check_col -= col_delta
            occupied_count = len(occupied_cells)
            target_row = row + row_delta * (occupied_count - 1)
            target_col = col + col_delta * (occupied_count - 1)
            if (0 <= target_row < GRID_SIZE and
                0 <= target_col < GRID_SIZE and
                (self.grid[target_row][target_col].occupancy == 'empty' or
                 self.grid[target_row][target_col].occupancy != player_color)):
                possible_moves.append((target_row, target_col))
        return possible_moves

    def is_connected(self, row, col, player_color, visited):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]
        stack = [(row, col)]
        connected_cells = 0
        while stack:
            r, c = stack.pop()
            if (r, c) not in visited:
                visited.add((r, c))
                connected_cells += 1
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and
                        self.grid[nr][nc].occupancy == player_color and
                        (nr, nc) not in visited):
                        stack.append((nr, nc))
        return connected_cells

    def check_win(self, player_color):
        visited = set()
        total_pieces = sum(1 for row in self.grid for cell in row
                           if cell.occupancy == player_color)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if (self.grid[row][col].occupancy == player_color and
                    (row, col) not in visited):
                    connected_cells = self.is_connected(row, col,
                                                        player_color,
                                                        visited)
                    if connected_cells == total_pieces:
                        return True
        return False

class Player:
    def __init__(self, color):
        self.color = color  # 'red' or 'blue'

class Game:
    def __init__(self):
        self.win = GraphWin("Lines of Action", 680, 680)
        self.win.setBackground("white")
        self.board = Board(self.win)
        self.players = [Player('red'), Player('blue')]
        self.current_player_index = 0

    def play(self):
        while True:
            current_player = self.players[self.current_player_index]
            print(f"{current_player.color.capitalize()}'s turn.")
            # Clear previous highlights
            self.board.clear_highlights()
            # Ask player to select a piece
            row, col = self.ask_player_for_move(current_player)
            print(f"{current_player.color.capitalize()} selected "
                  f"{chr(col + ord('A'))}{8 - row}")
            # Highlight selected cell
            self.board.highlight_cell(row, col, 'yellow')
            # Get possible moves
            possible_moves = self.board.get_possible_moves(
                row, col, current_player.color)
            if not possible_moves:
                print("No possible moves for this piece.")
                continue
            # Highlight possible moves
            self.board.highlight_possible_moves(possible_moves)
            # Move piece
            move_successful = self.move_piece(row, col, possible_moves,
                                              current_player.color)
            if move_successful:
                # Check for win conditions
                red_wins = self.board.check_win('red')
                blue_wins = self.board.check_win('blue')
                if red_wins and blue_wins:
                    print("It's a tie!")
                    break
                elif red_wins:
                    print("Red wins!")
                    break
                elif blue_wins:
                    print("Blue wins!")
                    break
                # Switch to next player
                self.current_player_index = 1 - self.current_player_index

    def ask_player_for_move(self, player):
        while True:
            click = self.win.getMouse()
            click_x, click_y = click.getX(), click.getY()
            col = int((click_x - MARGIN) // CELL_SIZE)
            row = int((GRID_SIZE - 1) - (click_y - MARGIN) // CELL_SIZE)
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                if self.board.grid[row][col].occupancy == player.color:
                    return row, col
                else:
                    print(f"Invalid selection. Please select a "
                          f"{player.color} piece.")
            else:
                print("Invalid click. Please click within the board.")

    def move_piece(self, start_row, start_col, possible_moves, player_color):
        while True:
            click = self.win.getMouse()
            click_x, click_y = click.getX(), click.getY()
            target_col = int((click_x - MARGIN) // CELL_SIZE)
            target_row = int((GRID_SIZE - 1) - (click_y - MARGIN) // CELL_SIZE)
            if 0 <= target_row < GRID_SIZE and 0 <= target_col < GRID_SIZE:
                if (target_row, target_col) in possible_moves:
                    self.board.move_piece(start_row, start_col,
                                          target_row, target_col,
                                          player_color)
                    print(f"{player_color.capitalize()} moved to "
                          f"{chr(target_col + ord('A'))}{8 - target_row}")
                    return True
                else:
                    print("Invalid move. Please select a highlighted cell.")
            else:
                print("Invalid click. Please click within the board.")

if __name__ == "__main__":
    game = Game()
    game.play()
