import graphics as g
import numpy as np

class Board:

    EMPTY = 0
    BLACK = 1
    WHITE = 2
    
    def __init__(self):
        self.win = g.GraphWin("Lines of Action", 400, 400, autoflush=False)
        self.win.setCoords(0.0, 0.0, 8.0, 8.0)
        self.board = [[Board.EMPTY for _ in range(8)] for _ in range(8)]
        for i in range(1, 7):
            self.board[0][i] = Board.BLACK
            self.board[7][i] = Board.BLACK
            self.board[i][0] = Board.WHITE
            self.board[i][7] = Board.WHITE

    def draw(self, movementable, selected_piece=None):
        self.win.delete('all')  # Clear the window before redrawing
        for x in range(8):
            for y in range(8):
                square = g.Rectangle(g.Point(x, y), g.Point(x + 1, y + 1))
                if (x, y) in movementable:
                    square.setFill('blue')
                else:
                    square.setFill('white')
                square.draw(self.win)

                if self.board[x][y] == Board.EMPTY:
                    continue  # No piece to draw
                elif self.board[x][y] == Board.WHITE:
                    color = 'red'
                elif self.board[x][y] == Board.BLACK:
                    color = 'black'
                circle = g.Circle(g.Point(x + 0.5, y + 0.5), 0.4)
                circle.setFill(color)
                circle.setOutline(color)
                circle.draw(self.win)

                # Highlight the selected piece
                if selected_piece == (x, y):
                    circle.setWidth(3)
                    circle.setOutline('yellow')

    def game(self):
        current_player = Board.BLACK  # BLACK makes the first move
        while True:
            self.draw([])
            print(f"Player {'BLACK' if current_player == Board.BLACK else 'WHITE'}'s turn.")
            movementable = []
            piece_selected = False
            mx, my = None, None

            while True:
                point = self.win.getMouse()
                x, y = int(np.floor(point.getX())), int(np.floor(point.getY()))
                if not (0 <= x < 8 and 0 <= y < 8):
                    print("Click within the board.")
                    continue

                if not piece_selected:
                    # Select a piece
                    if self.board[x][y] != current_player:
                        print("Please select one of your own pieces.")
                        continue
                    mx, my = x, y
                    # Get possible moves
                    movementable = self.check_similar_elements(mx, my)
                    if not movementable:
                        print("No valid moves for this piece. Please select another piece.")
                        continue
                    # Highlight the selected piece and possible moves
                    self.draw(movementable, selected_piece=(mx, my))
                    piece_selected = True
                else:
                    # Deselect the piece
                    if (x, y) == (mx, my):
                        print("Piece deselected.")
                        self.draw([])
                        piece_selected = False
                        mx, my = None, None
                        movementable = []
                    # Move the piece if the destination is valid
                    elif (x, y) in movementable:
                        nx, ny = x, y
                        # Move the piece
                        self.board[nx][ny] = self.board[mx][my]
                        self.board[mx][my] = Board.EMPTY
                        # Clear movementable highlights
                        self.draw([])
                        # Check for win conditions
                        winner = self.check_all_connected()
                        if winner:
                            self.draw([])
                            print(f"Player {'BLACK' if winner == Board.BLACK else 'WHITE'} wins!")
                            self.win.getMouse()  # Wait for a final click before closing
                            self.win.close()
                            return
                        # Switch players
                        current_player = Board.WHITE if current_player == Board.BLACK else Board.BLACK
                        break
                    else:
                        print("Invalid move or selection. Click on a highlighted square to move, or click the selected piece to deselect.")



    def count_pieces_in_line(self, x, y, dx, dy):
        count = 0
        x += dx
        y += dy
        while 0 <= x < 8 and 0 <= y < 8:
            if self.board[x][y] != Board.EMPTY:
                count += 1
            x += dx
            y += dy
        return count

    def is_path_clear(self, x, y, dx, dy, distance):
        x += dx
        y += dy
        for _ in range(distance - 1):
            if not (0 <= x < 8 and 0 <= y < 8):
                return False
            if self.board[x][y] != Board.EMPTY:
                return False
            x += dx
            y += dy
        return True

    def check_similar_elements(self, mx, my):
        # Directions: (dx, dy) pairs for 8 directions
        directions = [
            (-1, 0),   # left
            (1, 0),    # right
            (0, -1),   # down
            (0, 1),    # up
            (-1, -1),  # bottom-left
            (1, -1),   # bottom-right
            (-1, 1),   # top-left
            (1, 1)     # top-right
        ]

        movement_options = {}

        for i in range(0, len(directions), 2):
            dx1, dy1 = directions[i]
            dx2, dy2 = directions[i + 1]

            # Count in positive direction
            count_pos = self.count_pieces_in_line(mx, my, dx1, dy1)
            # Count in negative direction
            count_neg = self.count_pieces_in_line(mx, my, dx2, dy2)
            # Total count including the moving piece
            total_count = count_pos + count_neg + 1

            # Possible target positions in both directions
            target_positions = [
                (mx + dx1 * total_count, my + dy1 * total_count),
                (mx + dx2 * total_count, my + dy2 * total_count)
            ]

            for tx, ty in target_positions:
                if 0 <= tx < 8 and 0 <= ty < 8:
                    tx_int, ty_int = int(tx), int(ty)
                    # Check for obstructions
                    dx, dy = (dx1, dy1) if (tx_int, ty_int) == (mx + dx1 * total_count, my + dy1 * total_count) else (dx2, dy2)
                    if self.is_path_clear(mx, my, dx, dy, total_count):
                        # Avoid moving onto own piece
                        if self.board[tx_int][ty_int] != self.board[mx][my]:
                            movement_options[(tx_int, ty_int)] = True

        # Return the list of valid move coordinates
        return list(movement_options.keys())

    def dfs(self, x, y, color, visited):
        # Directions for all 8 possible moves: horizontal, vertical, and diagonal
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Stack-based DFS to avoid recursion depth issues
        stack = [(x, y)]
        visited.add((x, y))

        while stack:
            cx, cy = stack.pop()
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < 8 and 0 <= ny < 8 and (nx, ny) not in visited:
                    if self.board[nx][ny] == color:  # Only visit connected pieces of the same color
                        visited.add((nx, ny))
                        stack.append((nx, ny))

    def count_connected(self, color):
        # Count the number of connected components for the given color
        visited = set()
        components = 0

        for x in range(8):
            for y in range(8):
                if self.board[x][y] == color and (x, y) not in visited:
                    self.dfs(x, y, color, visited)
                    components += 1  # Each DFS traversal represents a connected component

        return components

    def check_all_connected(self):
        # Check if all pieces of a color are connected
        black_connected = self.count_connected(Board.BLACK) == 1
        white_connected = self.count_connected(Board.WHITE) == 1

        if black_connected and white_connected:
            print("It's a tie! Both players have connected all their pieces.")
            return 'TIE'
        elif black_connected:
            print("All BLACK pieces are connected.")
            return Board.BLACK
        elif white_connected:
            print("All WHITE pieces are connected.")
            return Board.WHITE
        else:
            return None  # No player has won yet
