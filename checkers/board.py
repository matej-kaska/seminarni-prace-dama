from .constants import BLACK, WHITE, ROWS, COLS, AQUA, CRIMSON
from .square import Square
from .man import Man
from .king import King

class Board:
    def __init__(self):
        self._squares = [[0 for _ in range(COLS)] for _ in range(ROWS)] # empty 2D list
        self.__create_board()

    @property
    def squares(self):
        return self._squares

    @squares.setter
    def squares(self, val):
        self._squares = val

    def __create_board(self):
        self.__add_squares() # _ = protected | __ = private
        self.__add_labels()
        self.__add_default_pieces()

    def __add_squares(self):
        for i in range(ROWS):
            for j in range(COLS):
                if i % 2 == 0:
                    self._squares[i][j] = Square(j, i, WHITE if j % 2 == 0 else BLACK)
                elif i % 2 == 1:
                    self._squares[i][j] = Square(j, i, WHITE if j % 2 == 1 else BLACK)
        
    def __add_labels(self):
        labels = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
        for j in range(COLS):
            for i in range(ROWS):
                self._squares[i][j].label = f"{labels[j]}{ROWS - i}"

    def __add_default_pieces(self):
        for i in range(ROWS):
            for j in range(COLS):
                if i % 2 == 0:
                    if i < 3 and j % 2 == 1:
                        self._squares[i][j].piece = Man(CRIMSON, "b")
                    elif i > 4 and j % 2 == 1:
                        self._squares[i][j].piece = Man(AQUA, "w")
                elif i % 2 == 1:
                    if i < 3 and j % 2 == 0:
                        self._squares[i][j].piece = Man(CRIMSON, "b")
                    elif i > 4 and j % 2 == 0:
                        self._squares[i][j].piece = Man(AQUA, "w")
    
    def clear_board(self):
        for i in range(ROWS):
            for j in range(COLS):
                self._squares[i][j].piece = None

    def draw_board(self, win):
        for i in range(ROWS):
            for j in range(COLS):
                self._squares[i][j].draw_square(win)

    def despawn_piece(self, killed):
        if killed:
            for pos in killed:
                y = int(pos[0])
                x = int(pos[1])
                self._squares[y][x].piece = None

    def spawn_king(self, y, x):
        color = self._squares[y][x].piece.color
        self._squares[y][x].piece = None
        if color == CRIMSON:
            team = "b"
        else: 
            team = "w"
        self._squares[y][x].piece = King(color, team)
    
    def restart_board(self):
        for i in range(ROWS):
            for j in range(COLS):
                self._squares[i][j].piece = None
                if i % 2 == 0:
                    if i < 3 and j % 2 == 1:
                        self._squares[i][j].piece = Man(CRIMSON, "b")
                    elif i > 4 and j % 2 == 1:
                        self._squares[i][j].piece = Man(AQUA, "w")
                elif i % 2 == 1:
                    if i < 3 and j % 2 == 0:
                        self._squares[i][j].piece = Man(CRIMSON, "b")
                    elif i > 4 and j % 2 == 0:
                        self._squares[i][j].piece = Man(AQUA, "w")