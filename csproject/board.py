import graphics as g
from vector import Vector
import numpy as nmp

class Board:

    EMPTY = 0
    BLACK = 1
    WHITE = 2
    white_coord = []
    black_coord = []
    
    def __init__(self):
        self.win = g.GraphWin("Lines of Action", 400, 400, autoflush = False)
        self.win.setCoords(0.0, 0.0, 8.0, 8.0)
        self.board = [[Board.EMPTY for i in range(8)] for i in range(8)]
        for i in range(1, 7):
            self.board[0][i] = Board.BLACK
            self.board[7][i] = Board.BLACK
            self.board[i][7] = Board.WHITE
            self.board[i][0] = Board.WHITE


    def draw(self, movementable):
        Board.white_coord = []
        Board.black_coord = []
        for x in range(8):
            for y in range(8):
                square = g.Rectangle(g.Point(x, y), g.Point(x + 1, y + 1))
                if (x, y) in movementable:
                    square.setFill('blue')
                elif (x, y) not in movementable:
                    square.setFill('white')
                square.draw(self.win)

                if self.board[x][y] == Board.EMPTY: 
                    color = 'white'
                if self.board[x][y] == Board.WHITE: 
                    color = 'red'
                    Board.white_coord.append((x, y))
                if self.board[x][y] == Board.BLACK: 
                    color = 'black'
                    Board.black_coord.append((x, y))
                circle = g.Circle(g.Point(x + 0.5, y + 0.5), 0.4)
                circle.setFill(color)
                circle.setOutline(color)
                circle.draw(self.win)

                #print("-----")
                #print(Board.white_coord)
                #print("-----")
                #print(Board.black_coord)

    ###########MOVING PIECES AROUND AND EATING THEM CRAP###############
    def game(self):
        counter = 0
        mv_allowed = True
        coordinate_W = Board.white_coord #Black make the 1st move
        coordinate_B = Board.black_coord #Black make the 1st move
        while mv_allowed:
            movementable = []
            point = self.win.getMouse()
            mx, my = int(nmp.floor(point.getX())), int(nmp.floor(point.getY()))
            #FOR THIS ONE YOU WILL DO SELECT AND MOVE THING IN ONE SCRIPT
            while (mx, my) in coordinate_B: #movement and selection code here
                
                ###########selection code#############
                movementable = self.check_similar_elements(mx, my)
                self.draw(movementable)
                #print(movementable)
                ######################################

                ###########movement code##############
                point = self.win.getMouse() #Get movement coordinates
                nx, ny = int(nmp.floor(point.getX())), int(nmp.floor(point.getY()))
                
                if (nx, ny) in movementable and self.board: #EATING CODE
                    if self.board[nx][ny] == Board.EMPTY:
                        self.board[mx][my], self.board[nx][ny] = self.board[nx][ny], self.board[mx][my]
                    elif self.board[nx][ny] != self.board[mx][my]:
                        self.board[mx][my], self.board[nx][ny] = self.board[nx][ny], self.board[mx][my]
                        self.board[mx][my] = Board.EMPTY


                    self.draw([])
                    mx, my, nx, ny = 0, 0, 0, 0
                    coordinate_W, coordinate_B = coordinate_B, coordinate_W #this will be done after the move was done
                    counter += 1
                    #print(counter)
                #######################################


                ############check for winner###############
                if counter == 2: #Movement code here
                    for x in range(8):
                        for y in range(8):
                            if self.board[x][y] == Board.WHITE: 
                                Board.white_coord.append((x, y))
                                coordinate_W = Board.white_coord
                            if self.board[x][y] == Board.BLACK: 
                                Board.black_coord.append((x, y))
                                coordinate_B = Board.black_coord
                    self.check_all_connected()
                    counter = 0
                    print("MV_NOT_ALLOWED")
                    break
                ###########################################


        print(mx, my)
        return mx, my
    

    def count_similar_in_direction(self, x, y, dx, dy):
        # Start from (x, y) and check in the direction (dx, dy)
        count = 0
        rows = len(self.board)
        cols = len(self.board[0])
        # Ensure that x, y, nx, and ny are integers
        x, y = int(x), int(y)
        # Traverse in the direction (dx, dy)
        nx, ny = x, y
        while 0 <= nx < rows and 0 <= ny < cols:
            if self.board[nx][ny] == Board.BLACK or self.board[nx][ny] == Board.WHITE:
                count += 1

            if self.board[x][y] == Board.WHITE:
                if self.board[nx][ny] == Board.BLACK:
                    print(f"black is {nx},{ny}")
            elif self.board[x][y] == Board.BLACK:
                if self.board[nx][ny] == Board.WHITE:
                    print(f"white is {nx},{ny}")
                    
            nx += dx
            ny += dy
            print(f"cycle is {nx},{ny}, piece is {x},{y}")


            # Ensure nx and ny remain integers after updating
            nx, ny = int(nx), int(ny)

        return count
    
    def check_similar_elements(self, mx, my):
        # Directions: (dx, dy) pairs for 8 directions
        directions = [
            (-1, 0),   # left
            (1, 0),    # right
            (0, -1),   # down
            (0, 1),    # up
            (-1, -1),  # bot-lef
            (-1, 1),   # top-lef
            (1, -1),   # bot-rit
            (1, 1)     # top-rit
        ]

        # Initialize the results for each direction
        up_count = 0
        down_count = 0
        left_count = 0
        right_count = 0
        top_left_diagonal_count = 0
        top_right_diagonal_count = 0
        bottom_left_diagonal_count = 0
        bottom_right_diagonal_count = 0
        
            # Traverse all the directions and accumulate the sums
        for dx, dy in directions:
            count = self.count_similar_in_direction(mx, my, dx, dy)
                ##########CALCULATE POSSIBLE MOVE COORDINATES###############
            if (dx, dy) == (0, 1):  # Up
                up_count = (float(mx), float(my + count))
                print(f"__up__ {count}")

            elif (dx, dy) == (0, -1):  # Down
                down_count = (float(mx), float(my - count))
                print(f"__down__ {count}")

            elif (dx, dy) == (-1, 0):  # Left
                left_count = (float(mx - count), float(my))
                print(f"__left__ {count}")

            elif (dx, dy) == (1, 0):  # Right
                right_count = (float(mx + count), float(my))
                print(f"__right__ {count}")

            elif (dx, dy) == (-1, 1):  # Top-left diagonal
                top_left_diagonal_count = (float(mx - count), float(my + count))
                print(f"__top left__ {count}")

            elif (dx, dy) == (1, 1):  # Top-right diagonal
                top_right_diagonal_count = (float(mx + count), float(my + count))
                print(f"__top right__ {count}")

            elif (dx, dy) == (-1, -1):  # Bottom-left diagonal
                bottom_left_diagonal_count = (float(mx - count), float(my - count))
                print(f"__bot left__ {count}")

            elif (dx, dy) == (1, -1):  # Bottom-right diagonal
                bottom_right_diagonal_count = (float(mx + count), float(my - count))
                print(f"__bot right__ {count}")

        available_move_coordinates = [up_count, down_count, 
                                      left_count, right_count, 
                                      top_left_diagonal_count, top_right_diagonal_count, 
                                      bottom_left_diagonal_count, bottom_right_diagonal_count]
        
        print(available_move_coordinates)
        # Return the results as a list
        return available_move_coordinates




    

    ###########WINNER CHECKER SHIT#############
    def dfs(self, x, y, color, visited):
        # Directions for all 8 possible moves: horizontal, vertical, and diagonal
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
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
        # Count the number of connected pieces of the given color (1 for BLACK, 2 for WHITE)
        visited = set()
        count = 0

        # Find all starting points for DFS (cells containing the given color)
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == color and (x, y) not in visited:
                    # Start DFS from this unvisited piece
                    self.dfs(x, y, color, visited)
                    count += 1  # Each DFS corresponds to one connected component

        return count


    def check_all_connected(self):
        # Check if all BLACK pieces are connected
        black_connected = self.count_connected(Board.BLACK) == 1
        white_connected = self.count_connected(Board.WHITE) == 1
        
        if black_connected:
            print("All BLACK pieces are connected.")
        else:
            print("BLACK pieces are not all connected.")
        
        if white_connected:
            print("All WHITE pieces are connected.")
        else:
            print("WHITE pieces are not all connected.")
###################################################################
