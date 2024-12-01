from board import Board
# from boardz import Board
# from boardzz import Board

def main():
    board = Board()
    while True:
        board.draw([])
        board.game()
        # board.check_all_connected()


if __name__ == '__main__':
    main()