from .constants import BLACK, WHITE, RED, BLUE, ROWS, COLS
from .square import Square
from .piece import Piece

class Board:
    def __init__(self):
        self._squares = [[0 for _ in range(COLS)] for _ in range(ROWS)] # empty 2D list

    @property
    def squares(self):
        return self._squares

    @squares.setter
    def squares(self, val):
        self._squares = val

    def create_board(self):
        for i in range(ROWS):
            for j in range(COLS):
                # if row is even
                if i % 2 == 0:
                    # add white square if col is even else add black one
                    self._squares[i][j] = Square(j, i, WHITE if j % 2 == 0 else BLACK)
                    # add pieces to their correct starting pos
                    if i < 3 and j % 2 == 1:
                        self._squares[i][j].piece = Piece(RED, i, j)
                    elif i > 4 and j % 2 == 1:
                        self._squares[i][j].piece = Piece(BLUE, i, j)
                # if row is odd
                elif i % 2 == 1:
                    # add white square if col is odd else add black one
                    self._squares[i][j] = Square(j, i, WHITE if j % 2 == 1 else BLACK)
                    # add pieces to their correct starting pos
                    if i < 3 and j % 2 == 0:
                        self._squares[i][j].piece = Piece(RED, i, j)
                    elif i > 4 and j % 2 == 0:
                        self._squares[i][j].piece = Piece(BLUE, i, j)

    def draw_board(self, win):
        for i in range(ROWS):
            for j in range(COLS):
                self._squares[i][j].draw_square(win)

    def despawn_piece(self, y, x):
        self._squares[y][x].piece = None