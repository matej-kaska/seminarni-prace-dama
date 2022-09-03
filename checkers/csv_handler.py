from tkinter import filedialog, messagebox, Tk
import csv
from checkers.constants import CRIMSON, AQUA, COLS, ROWS
from checkers.man import Man
from checkers.king import King

class CSV_Handler:
    def __read_csv(self):
        try:
            root = Tk()
            root.wm_withdraw()
            file = filedialog.askopenfilename()

            if file == "": return
            
            with open(file, "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                dict = { rows[0].strip().upper():rows[1].strip().lower() for rows in csv_reader if "".join(rows).strip() }

                if len(dict) == 0 : raise Exception("Empty csv")
                if len(dict) > 24: raise Exception("Too many pieces")
                
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
                
                return dict
        except:
            messagebox.showerror(title="Error", message="Wrong file format!")
        finally:
            root.destroy()

    def load_from_csv(self, board):
        dict = self.__read_csv()
        if dict is None: return
        board.clear_board()
        for i in range(COLS):
            for j in range(ROWS):
                label = board.squares[i][j].label
                if label in dict:
                    if dict[label] == "b":
                        board.squares[i][j].piece = Man(CRIMSON, "b")
                    elif dict[label] == "bb":
                        board.squares[i][j].piece = King(CRIMSON, "b")
                    elif dict[label] == "w":
                        board.squares[i][j].piece = Man(AQUA, "w")
                    elif dict[label] == "ww":
                        board.squares[i][j].piece = King(AQUA, "w")

    def __get_pieces(self, board):
        pieces_dict = {}
        for i in range(ROWS):
            for j in range(COLS):
                if board.squares[i][j].piece is not None:
                    piece_type = type(board.squares[i][j].piece)
                    piece_color = board.squares[i][j].piece.color
                    if piece_type == Man and piece_color == CRIMSON:
                        pieces_dict.update({board.squares[i][j].label: "b"})
                    elif piece_type == King and piece_color == CRIMSON:
                        pieces_dict.update({board.squares[i][j].label: "bb"})
                    elif piece_type == Man and piece_color == AQUA:
                        pieces_dict.update({board.squares[i][j].label: "w"})
                    elif piece_type == King and piece_color == AQUA:
                        pieces_dict.update({board.squares[i][j].label: "ww"})
        return pieces_dict

    def save_to_csv(self, board):
        try:
            pieces_dict = self.__get_pieces(board)
            root = Tk()
            root.wm_withdraw()
            file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=(("CSV file", "*.csv"), ("All Files", "*.*")))

            if file == "": return

            with open(file, "w") as file:
                for label, piece in pieces_dict.items():
                    file.write(f"{label},{piece}\n")           
        except:
            messagebox.showerror(title="Error", message="Something went wrong :(")
        finally:
            root.destroy()