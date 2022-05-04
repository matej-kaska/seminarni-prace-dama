from .constants import BLACK, WHITE, RED, BLUE, ROWS, COLS, AQUA, CRIMSON
from .square import Square
from .piece import Piece
from .king import King
import csv

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
            dict = { rows[0].strip():rows[1].strip() for rows in csvreader if rows }        
            if len(dict) > 24: raise Exception("Too many pieces")
            pos_squares = ( # scuffed but works
                    "A1", "A3", "A5", "A7",
                    "B2", "B4", "B6", "B8",
                    "C1", "C3", "C5", "C7",
                    "D2", "D4", "D6", "D8",
                    "E1", "E3", "E5", "E7",
                    "F2", "F4", "F6", "F8",
                    "G1", "G3", "G5", "G7",
                    "H2", "H4", "H6", "H8"
                )
                         
            label = ""
            for i in range(COLS):
                for j in range(ROWS):
                    label = self._squares[i][j].label
                    if label in dict and label in pos_squares:
                        if dict[label] == "b":
                            self._squares[i][j].piece = Piece(RED)
                        elif dict[label] == "bb":
                            self._squares[i][j].piece = King(CRIMSON)
                        elif dict[label] == "w":
                            self._squares[i][j].piece = Piece(RED)
                        elif dict[label] == "ww":
                            self._squares[i][j].piece = King(AQUA)    
        except:
            print("Wrong csv file format - switched to default game")
            self.__add_default_pieces()

    def __add_default_pieces(self):
        for i in range(ROWS):
            for j in range(COLS):
                if i % 2 == 0:
                    if i < 3 and j % 2 == 1:
                        self._squares[i][j].piece = Piece(RED)
                    elif i > 4 and j % 2 == 1:
                        self._squares[i][j].piece = Piece(BLUE)
                elif i % 2 == 1:
                    if i < 3 and j % 2 == 0:
                        self._squares[i][j].piece = Piece(RED)
                    elif i > 4 and j % 2 == 0:
                        self._squares[i][j].piece = Piece(BLUE)

    def draw_board(self, win):
        for i in range(ROWS):
            for j in range(COLS):
                self._squares[i][j].draw_square(win)

    def despawn_piece(self, y, x):
        self._squares[y][x].piece = None