__author__ = 'Askar Takhirov'

"""

Lines of Action (LOA) Game

This is a version of the Lines of Action game where two players take turns playing on the same machine. 
The game is played with two colors: red and blue. Red always starts first.

In the game, each player controls pieces of their color, and the objective is to connect all of their pieces 
into one contiguous group. Players take turns moving their pieces according to the rules of the game, 
which involve moving in lines across the board in various directions.

The game is played on an 8x8 grid, and players must strategically plan their moves to outmaneuver their opponent.
The game ends when one player successfully connects all of their pieces or if the game reaches a tie.

Key Features:
- 2-player turn-based gameplay
- Red player always goes first
- Playable on the same machine
- The board is displayed graphically with cells representing each piece.
- Possible moves for each piece are highlighted in yellow for easy selection.
- Each piece can move horizontally, vertically, or diagonally in any direction, as long as it moves along 
  a line and follows the rules of movement:
    * Pieces move by jumping over a number of squares equal to the number of pieces in the line.
    * A player can move a piece to a valid empty or enemy-occupied cell.
    * The eight possible movement directions are:
        - Horizontal (left and right)
        - Vertical (up and down)
        - Diagonal (four directions: up-left, up-right, down-left, down-right)
        
    * The player selects the cell to move to by clicking on it in the graphical interface. 
    * Invalid selections or moves outside the allowed directions are rejected, and the player is prompted to try again.

How the Game Works:
- On each turn, the player selects one of their pieces by clicking on it in the window.
- After selecting the piece, the possible valid moves are highlighted in yellow on the board.
- The player then clicks on a valid destination cell to move their piece to that location.
- The game continues with alternating turns between the two players until one player wins or the game is tied.

"""

from graphics import *

GRID_SIZE = 8  # 8x8 grid
CELL_SIZE = 60  # Size of each square cell
MARGIN = 100  # Margin from the edges of the window

def initialize_board():

    """

    Initializes the game board for Lines of Action.

    The board is an 8x8 grid represented as a list of lists.
    Each cell is a dictionary containing:
        - 'occupancy': The current state of the cell ('empty', 'blue', or 'red').
        - 'row': The row number (1 to 8, top to bottom).
        - 'column': The column label ('A' to 'H', left to right).

    Specific initial configurations:
        - The top row (B8-G8) and the bottom row (B1-G1) are occupied by blue pieces.
        - The left column (A2-A7) and the right column (H2-H7) are occupied by red pieces.

    """

    board = []

    # Create the grid structure with default empty cells
    for row in range(GRID_SIZE):
        board_row = []
        for col in range(GRID_SIZE):
            cell = {
                'occupancy': 'empty',  # Default: all cells are initially empty
                'row': 8 - row,  # Map rows to numbers 8 (top) to 1 (bottom)
                'column': chr(65 + col)  # Map columns to letters A-H
            }
            board_row.append(cell)
        board.append(board_row)

    # Initialize blue pieces: Top and bottom rows from columns B to G
    for col in range(1, 7):  # Columns 1 to 6 correspond to B to G
        board[0][col]['occupancy'] = 'blue'  # Top row (B8-G8)
        board[7][col]['occupancy'] = 'blue'  # Bottom row (B1-G1)

    # Initialize red pieces: Left and right columns from rows 2 to 7
    for row in range(1, 7):  # Rows 1 to 6 correspond to A2-A7 and H2-H7
        board[row][0]['occupancy'] = 'red'  # Left column (A2-A7)
        board[row][7]['occupancy'] = 'red'  # Right column (H2-H7)

    return board

def fill_cell_background(win, board):

    """

    Fills the background of each cell on the board based on its occupancy.

    The function iterates through the game board and colors each cell according to its occupancy:
        - 'red' for cells occupied by red pieces.
        - 'blue' for cells occupied by blue pieces.
        - 'white' for empty cells.

    The function uses the graphics library to draw colored rectangles over the board.

    Parameters:
        win: The graphics window where the board is displayed.
        board: A 2D list representing the game board, where each cell contains an 'occupancy' key.

    """

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # Calculate the coordinates of the cell
            x1 = MARGIN + col * CELL_SIZE
            y1 = MARGIN + (GRID_SIZE - row - 1) * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            # Determine the fill color based on occupancy
            if board[row][col]['occupancy'] == 'red':
                fill_color = 'red'
            elif board[row][col]['occupancy'] == 'blue':
                fill_color = 'royalblue'
            else:
                fill_color = 'antiquewhite'

            # Create and draw the rectangle with the chosen color
            rect = Rectangle(Point(x1, y1), Point(x2, y2))
            rect.setFill(fill_color)  # Set the fill color of the rectangle
            rect.setWidth(0)  # Remove the rectangle's border
            rect.draw(win)  # Draw the rectangle on the window

def draw_grid(win, board):

    """

    Draws the game grid and labels for the Lines of Action game.

    The function creates an 8x8 grid with each cell labeled to show its:
        - Occupancy: 'empty', 'blue', or 'red'.
        - Row: Number from 8 to 1.
        - Column: Letter from A to H.

    It also adds:
        - Column labels (A-H) at the top and bottom of the grid.
        - Row labels (1-8) on the left and right sides of the grid.

    Parameters:
        win: The graphics window where the grid and labels are drawn.
        board: A 2D list representing the game board.

    """

    # Draw grid cells and their labels
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # Calculate the coordinates of the current cell
            x1 = MARGIN + col * CELL_SIZE
            y1 = MARGIN + (GRID_SIZE - row - 1) * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            
            # Draw the cell
            rect = Rectangle(Point(x1, y1), Point(x2, y2))
            rect.setWidth(2)
            rect.draw(win)

            # Add a label to display cell properties (occupancy, row, column)
            label = Text(
                Point(x1 + CELL_SIZE / 2, y1 + CELL_SIZE / 2),
                f"{board[row][col]['occupancy']}\n{board[row][col]['column']}{board[row][col]['row']}"
            )
            label.setSize(7)
            label.setTextColor('black')  # Ensure text is visible
            label.draw(win)

    # Draw column labels (A-H) at the top and bottom
    for col in range(GRID_SIZE):
        # Top column labels
        x_label = MARGIN + col * CELL_SIZE + CELL_SIZE / 2
        y_label_top = MARGIN - 20
        col_label_top = Text(Point(x_label, y_label_top), chr(65 + col))  # 'A' starts at ASCII 65
        col_label_top.setSize(12)
        col_label_top.setStyle('bold')
        col_label_top.setTextColor('black')
        col_label_top.draw(win)

        # Bottom column labels
        y_label_bottom = MARGIN + GRID_SIZE * CELL_SIZE + 20
        col_label_bottom = Text(Point(x_label, y_label_bottom), chr(65 + col))
        col_label_bottom.setSize(12)
        col_label_bottom.setStyle('bold')
        col_label_bottom.setTextColor('black')
        col_label_bottom.draw(win)

    # Draw row labels (1-8) on the left and right
    for row in range(GRID_SIZE):
        # Left row labels
        x_label_left = MARGIN - 20
        y_label = MARGIN + (GRID_SIZE - row - 1) * CELL_SIZE + CELL_SIZE / 2
        row_label_left = Text(Point(x_label_left, y_label), str(GRID_SIZE - row))
        row_label_left.setSize(12)
        row_label_left.setStyle('bold')
        row_label_left.setTextColor('black')
        row_label_left.draw(win)

        # Right row labels
        x_label_right = MARGIN + GRID_SIZE * CELL_SIZE + 20
        row_label_right = Text(Point(x_label_right, y_label), str(GRID_SIZE - row))
        row_label_right.setSize(12)
        row_label_right.setStyle('bold')
        row_label_right.setTextColor('black')
        row_label_right.draw(win)

def highlight_selected_cell(win, row, col):

    """

    Highlights the selected cell on the game board by drawing a yellow outline around it.

    The function calculates the coordinates of the selected cell based on the provided
    row and column indices and draws a rectangle with a yellow outline around the cell.
    The outline is slightly inset to ensure it stays within the boundaries of the cell.

    Parameters:
        win: The graphics window where the selection highlight is drawn.
        row: The row index (0 to 7) of the selected cell.
        col: The column index (0 to 7) of the selected cell.

    """

    # Calculate the top-left and bottom-right coordinates of the selected cell
    x1 = MARGIN + col * CELL_SIZE
    y1 = MARGIN + (GRID_SIZE - row - 1) * CELL_SIZE
    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE

    # Adjust the coordinates to add a slight padding, ensuring the outline fits within the cell
    outline_padding = 2  # Padding to ensure the outline stays inside the cell
    x1 += outline_padding
    y1 += outline_padding
    x2 -= outline_padding
    y2 -= outline_padding

    # Create a yellow outline for the selected cell
    outline = Rectangle(Point(x1, y1), Point(x2, y2))
    outline.setOutline("yellow")  # Set the color of the outline
    outline.setWidth(5)  # Set the thickness of the outline
    outline.draw(win)  # Draw the outline on the graphics window

def highlight_possible_moves(win, board, row, col, current_player):

    """

    Highlights the possible moves for a selected piece on the game board.

    The function calculates all possible moves for the piece located at the given row and column.
    It considers all 8 directions (horizontal, vertical, and diagonal), and highlights the valid
    moves where the target cell is either empty or occupied by the opponent's piece.

    Parameters:
        win: The graphics window where the moves are highlighted.
        board: A 2D list representing the game board, where each cell contains an 'occupancy' key.
        row: The row index (0 to 7) of the selected piece.
        col: The column index (0 to 7) of the selected piece.
        current_player: The player whose turn it is. Used to check for opponent pieces.

    Returns:
        A list of tuples representing the valid (row, col) positions of possible moves.

    """

    possible_moves = []

    # Directions as (row_delta, col_delta) representing movement in 8 directions
    directions = [
        (0, 1),   # Horizontal right
        (0, -1),  # Horizontal left
        (1, 0),   # Vertical down
        (-1, 0),  # Vertical up
        (1, 1),   # Diagonal down-right
        (-1, -1), # Diagonal up-left
        (1, -1),  # Diagonal down-left
        (-1, 1)   # Diagonal up-right
    ]

    # For each direction, check how far we can move
    for direction in directions:
        row_delta, col_delta = direction
        occupied_cells = []  # To track the occupied cells in this direction

        # Check forward and backward in the current direction
        # Forward direction: Move in the given direction (row_delta, col_delta)
        check_row, check_col = row, col
        while 0 <= check_row < GRID_SIZE and 0 <= check_col < GRID_SIZE:
            if board[check_row][check_col]['occupancy'] != 'empty':
                occupied_cells.append((check_row, check_col))  # Track occupied cells
            check_row += row_delta
            check_col += col_delta

        # Reverse direction: Move in the opposite direction (-row_delta, -col_delta)
        check_row, check_col = row, col
        while 0 <= check_row < GRID_SIZE and 0 <= check_col < GRID_SIZE:
            if board[check_row][check_col]['occupancy'] != 'empty':
                occupied_cells.append((check_row, check_col))  # Track occupied cells
            check_row -= row_delta
            check_col -= col_delta

        # The number of occupied cells determines the maximum movement distance
        occupied_count = len(occupied_cells)

        # Calculate the target position based on the occupied count
        target_row = row + row_delta * (occupied_count - 1)
        target_col = col + col_delta * (occupied_count - 1)

        # Check if the target position is within bounds and valid for a move
        if (
            0 <= target_row < GRID_SIZE and
            0 <= target_col < GRID_SIZE and
            (board[target_row][target_col]['occupancy'] == 'empty' or 
             board[target_row][target_col]['occupancy'] != current_player)
        ):
            # Add valid target cell to possible moves
            possible_moves.append((target_row, target_col))

    # Highlight the valid moves on the grid with a green outline
    for move_row, move_col in possible_moves:
        # Calculate the top-left and bottom-right coordinates for the move cell
        x1 = MARGIN + move_col * CELL_SIZE
        y1 = MARGIN + (GRID_SIZE - move_row - 1) * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE

        # Adjust the coordinates for the outline to stay inside the cell
        outline_padding = 2  # Padding to ensure the outline stays inside the cell
        x1 += outline_padding
        y1 += outline_padding
        x2 -= outline_padding
        y2 -= outline_padding

        # Draw a green outline around the valid move
        outline = Rectangle(Point(x1, y1), Point(x2, y2))
        outline.setOutline("green")  # Set the outline color to green
        outline.setWidth(5)  # Set the outline thickness
        outline.draw(win)  # Draw the outline on the window

    # Return the list of possible moves
    return possible_moves

def move_piece(win, board, start_row, start_col, possible_moves, current_player):
    """
    Handles the movement of a piece for the current player via mouse clicks.

    This function waits for the player to click on a target cell for the move, validates the target
    based on the highlighted possible moves, updates the board, and redraws it.

    Parameters:
        win: The graphics window where the updated game board is drawn.
        board: A 2D list representing the game board, where each cell contains an 'occupancy' key.
        start_row: The row index (0 to 7) of the piece's current position.
        start_col: The column index (0 to 7) of the piece's current position.
        possible_moves: A list of valid (row, col) positions where the piece can move.
        current_player: The player whose turn it is (either 'red' or 'blue').

    Returns:
        bool: True if the move is successfully made, otherwise False.
    """
    while True:
        # Wait for a mouse click to get the target cell
        click = win.getMouse()
        click_x, click_y = click.getX(), click.getY()

        # Convert the click coordinates to grid indices
        target_col = int((click_x - MARGIN) // CELL_SIZE)
        target_row = int((GRID_SIZE - 1) - (click_y - MARGIN) // CELL_SIZE)

        # Ensure the click is within the board boundaries
        if 0 <= target_row < GRID_SIZE and 0 <= target_col < GRID_SIZE:
            # Check if the target cell is a valid move
            if (target_row, target_col) in possible_moves:
                # Move the piece and update the board
                board[target_row][target_col]['occupancy'] = current_player
                board[start_row][start_col]['occupancy'] = 'empty'

                # Update the graphical board
                fill_cell_background(win, board)
                draw_grid(win, board)

                # Convert column index to letter (A-H)
                column_letter = chr(target_col + ord('A'))

                # Convert row index to number (8-1)
                row_number = 8 - target_row

                # Print the move in the desired format (e.g., B8, C1, etc.)
                print(f"{current_player.capitalize()} piece moved to {column_letter}{row_number}")

                return True  # Indicate the move was successful
            else:
                print("Invalid move. Please click on a highlighted cell.")
        else:
            print("Invalid click. Please click within the board.")

def ask_player_for_move(win, current_player, board):
    """
    Prompts the player to select a cell by clicking on it on the graphical board.

    Parameters:
        win: The graphical window where the game board is displayed.
        current_player: The player whose turn it is (either 'red' or 'blue').
        board: A 2D list representing the game board, where each cell contains an 'occupancy' key.

    Returns:
        tuple: A tuple (row, col) representing the selected cell's coordinates on the board.
    """
    while True:
        # Wait for a mouse click
        click = win.getMouse()
        click_x, click_y = click.getX(), click.getY()

        # Convert pixel coordinates to grid indices
        col = int((click_x - MARGIN) // CELL_SIZE)
        row = int((GRID_SIZE - 1) - (click_y - MARGIN) // CELL_SIZE)

        # Ensure indices are within bounds
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            # Check if the selected cell belongs to the current player
            if board[row][col]['occupancy'] == current_player:
                return row, col  # Return the selected row and column indices
            else:
                print(f"Invalid selection. Please select a cell that belongs to the {current_player} player.")
        else:
            # Handle out-of-bound clicks
            print("Invalid click. Please click within the board.")

def is_connected(board, row, col, player, visited):

    """

    Checks if the current player's piece at the given position is connected to other pieces.

    This function performs a Depth-First Search (DFS) using an iterative approach with a stack
    to explore all connected pieces of the current player starting from the specified cell.
    It tracks all visited cells to avoid reprocessing them.

    Parameters:
        board: A 2D list representing the game board, where each cell contains an 'occupancy' key.
        row: The row index of the current player's piece being checked.
        col: The column index of the current player's piece being checked.
        player: A string representing the current player ('red' or 'blue').
        visited: A set to keep track of visited cells to avoid processing the same cell multiple times.

    Returns:
        int: The number of connected pieces of the current player starting from the given cell.

    """

    # Directions for the 8 possible moves (up, down, left, right, diagonals)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    # Initialize the stack for DFS and the count of connected cells
    stack = [(row, col)]
    connected_cells = 0
    
    # Iteratively explore the board using a stack for DFS
    while stack:
        r, c = stack.pop()  # Pop the top cell from the stack
        
        # If the cell hasn't been visited, mark it as visited and increase the count
        if (r, c) not in visited:
            visited.add((r, c))
            connected_cells += 1

            # Explore all 8 possible directions from the current cell
            for dr, dc in directions:
                nr, nc = r + dr, c + dc  # New row and column indices

                # Ensure the new position is within the bounds of the board and is the player's piece
                if 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc]['occupancy'] == player:
                    # If the new cell is not visited, add it to the stack
                    if (nr, nc) not in visited:
                        stack.append((nr, nc))

    # Return the total number of connected cells found for the current player
    return connected_cells

def check_win(board, player):

    """

    Checks if the given player has won the game by having all their pieces connected.

    This function first counts the total number of pieces for the given player. Then, 
    it checks if all of the player's pieces are connected on the board. It does this by
    performing a Depth-First Search (DFS) starting from any unvisited piece and checking 
    if all the pieces can be reached.

    Parameters:
        board: A 2D list representing the game board, where each cell contains an 'occupancy' key.
        player: A string representing the current player ('red' or 'blue').

    Returns:
        bool: True if the player has won (i.e., all their pieces are connected), False otherwise.

    """

    # Set to keep track of visited cells during the DFS
    visited = set()

    # Count the total number of pieces for the player on the board
    total_player_pieces = 0  # Variable to store the total number of pieces for the player
    
    # Loop through the board to count all of the player's pieces
    for row in range(8):
        for col in range(8):
            if board[row][col]['occupancy'] == player:
                total_player_pieces += 1  # Increment the counter for each player's piece
    
    # Check if all of the player's pieces are connected
    for row in range(8):
        for col in range(8):
            if board[row][col]['occupancy'] == player and (row, col) not in visited:
                # Start DFS from the first unvisited piece of the player
                connected_cells = is_connected(board, row, col, player, visited)

                # If the number of connected cells equals the total pieces, player has won
                if connected_cells == total_player_pieces:
                    return True  # All pieces are connected, so the player wins

    # If not all pieces are connected, the player has not won
    return False

def main():
    """
    The main function that manages the flow of the Lines of Action game.
    
    This function initializes the game board, manages turns between two players (red and blue),
    and handles user inputs for selecting and moving pieces. The game continues until one player
    wins or the game ends in a tie. The graphical interface is updated after each move.
    """

    # Initialize the game board with pieces placed in their starting positions
    board = initialize_board()  
    win = GraphWin("8x8 Grid", 680, 680)  # Create a graphical window for the board
    win.setBackground("white")  # Set the background color of the window

    # Fill each cell's background with the appropriate color (red, blue, or empty)
    fill_cell_background(win, board)
    
    # Draw the grid structure with labels for rows and columns
    draw_grid(win, board)

    # The game starts with the red player
    current_player = 'red'  

    while True:
        # Display whose turn it is
        print(f"{current_player.capitalize()}'s turn.")
        
        # Prompt the current player to select a piece
        row, col = ask_player_for_move(win, current_player, board)  # Pass `win` as an argument
        print(f"{current_player.capitalize()} player selected cell at {chr(col + ord('A'))}{8 - row}")

        # Highlight the selected cell in yellow to indicate the player's choice
        highlight_selected_cell(win, row, col)

        # Highlight possible valid moves for the selected piece
        possible_moves = highlight_possible_moves(win, board, row, col, current_player)
        
        # Prompt the current player to move their piece to a valid destination
        move_successful = move_piece(win, board, row, col, possible_moves, current_player)
        
        # If the move was successful, check for win conditions
        if move_successful:
            # Check if either player has won or if it's a tie
            red_wins = check_win(board, 'red')
            blue_wins = check_win(board, 'blue')

            if red_wins and blue_wins:
                print("It's a tie! Both players connected their pieces simultaneously.")
                break  # End the game in a tie
            elif red_wins:
                print("Red wins!")
                break  # End the game with a red victory
            elif blue_wins:
                print("Blue wins!")
                break  # End the game with a blue victory
            
            # Switch turns between players
            current_player = 'blue' if current_player == 'red' else 'red'

if __name__ == "__main__":
    main()