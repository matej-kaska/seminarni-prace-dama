from .constants import BLACK, WHITE, ROWS, COLS, AQUA, CRIMSON
from .square import Square
from .man import Man
from .king import King
import csv
import tkinter
import tkinter.filedialog
import tkinter.messagebox

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

    def add_pieces_from_csv(self):
        try:
            root = tkinter.Tk()
            root.wm_withdraw()
            filename = tkinter.filedialog.askopenfilename()
            if filename == "":
                return
            with open(filename) as file:
                csvreader = csv.reader(file)
                dict = { rows[0].strip().upper():rows[1].strip().lower() for rows in csvreader if "".join(rows).strip() } 
                if len(dict) == 0:
                    raise Exception("Empty CSV")  
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
                self.__clear_board()
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
            tkinter.messagebox.showerror(title="Error", message="Wrong file format!")
    
    def save_game(self):
        try:
            pieces = {}
            for i in range(ROWS):
                for j in range(COLS):
                    if self._squares[i][j].piece is not None:
                        if type(self._squares[i][j].piece) == Man and self._squares[i][j].piece.color == CRIMSON:
                            piece = "b"
                        elif type(self._squares[i][j].piece) == King and self._squares[i][j].piece.color == CRIMSON:
                            piece = "bb"
                        elif type(self._squares[i][j].piece) == Man and self._squares[i][j].piece.color == AQUA:
                            piece = "w"  
                        elif type(self._squares[i][j].piece) == King and self._squares[i][j].piece.color == AQUA:
                            piece = "ww"    
                        pieces.update({self._squares[i][j].label: piece})

            root = tkinter.Tk()
            root.wm_withdraw()
                
            filename = tkinter.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=(("CSV file", "*.csv"), ("All Files", "*.*")))
            if filename == "":
                return
            with open(filename, "w") as file:
                for key, value in pieces.items():
                    file.write(f"{key},{value}\n")
        except:
            tkinter.messagebox.showerror(title="Error", message="Something went wrong :(")

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
    
    def __clear_board(self):
        for i in range(ROWS):
            for j in range(COLS):
                if self._squares[i][j].piece is not None:
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