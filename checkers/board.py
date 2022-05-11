from .constants import BLACK, WHITE, ROWS, COLS, AQUA, CRIMSON
from .square import Square
from .man import Man
from .king import King
import csv

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
        self.__add_pieces_from_csv()

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

    def __add_pieces_from_csv(self):
        try:
            file = open('data.csv')
            csvreader = csv.reader(file)
            dict = { rows[0].strip().upper():rows[1].strip().lower() for rows in csvreader if "".join(rows).strip() } 
            labels = (
                "A1", "A3", "A5", "A7",
                "B2", "B4", "B6", "B8",
                "C1", "C3", "C5", "C7",
                "D2", "D4", "D6", "D8",
                "E1", "E3", "E5", "E7",
                "F2", "F4", "F6", "F8",
                "G1", "G3", "G5", "G7",
                "H2", "H4", "H6", "H8"
            )
            pieces = ("b", "bb", "w", "ww")
            for label, piece in dict.items():
                if label not in labels or piece not in pieces:
                    raise Exception("Wrong format")  
            if len(dict) > 24: raise Exception("Too many pieces")                 
            label = ""
            for i in range(COLS):
                for j in range(ROWS):
                    label = self._squares[i][j].label
                    if label in dict and self._squares[i][j].color == BLACK:
                        if dict[label] == "b":
                            self._squares[i][j].piece = Man(CRIMSON, "b")
                        elif dict[label] == "bb":
                            self._squares[i][j].piece = King(CRIMSON, "b")
                        elif dict[label] == "w":
                            self._squares[i][j].piece = Man(AQUA, "w")
                        elif dict[label] == "ww":
                            self._squares[i][j].piece = King(AQUA, "w")    
        except:
            print("Wrong csv file format - switched to default game")
            self.__add_default_pieces()

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