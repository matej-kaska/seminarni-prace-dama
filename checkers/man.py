import pygame
from .piece import Piece
from .constants import AQUA, CRIMSON, ROWS, COLS
from anytree import Node, PreOrderIter, RenderTree

class Man(Piece):
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val):
        self._color = val

    @property
    def team(self):
        return self._team

    @team.setter
    def team(self, val):
        self._team = val

    @property
    def default_color(self):
        return self._default_color

    @default_color.setter
    def default_color(self, val):
        self._default_color = val

    def draw_piece(self, square, win):
        pygame.draw.ellipse(
            win,
            self._color,
            (square.x * square.size + square.size / 5,
            square.y * square.size + square.size / 5,
            square.size / 5 * 3,
            square.size / 5 * 3)
            )

    def get_possible_moves(self, y, x, board):
        root = Node(str(y) + str(x))
        if board.squares[y][x].piece is not None:
            if self.team == "w":
                if y - 1 >= 0 and x + 1 < COLS:
                    if board.squares[y-1][x+1].piece is None:
                        Node(str(y-1) + str(x+1), parent=root)
                    elif y - 2 >= 0 and x + 2 < COLS:
                        if board.squares[y-2][x+2].piece is None and board.squares[y-1][x+1].piece.team == "b":
                            Node(str(y-2) + str(x+2) + str(y-1) + str(x+1), parent=root)
                            self.chaining(y-2, x+2, board)

                if y - 1 >= 0 and x - 1 >= 0:
                    if board.squares[y-1][x-1].piece is None:
                        Node(str(y-1) + str(x-1), parent=root)
                    elif y - 2 >= 0 and x - 2 >= 0:
                        if board.squares[y-2][x-2].piece is None and board.squares[y-1][x-1].piece.team == "b":
                            Node(str(y-2) + str(x-2) + str(y-1) + str(x-1), parent=root)
                            self.chaining(y-2, x-2, board)

            if self.team == "b":
                if y + 1 < ROWS and x + 1 < COLS:
                    if board.squares[y+1][x+1].piece is None:
                        Node(str(y+1) + str(x+1), parent=root)
                    elif y + 2 < ROWS and x + 2 < COLS:
                        if board.squares[y+2][x+2].piece is None and board.squares[y+1][x+1].piece.team == "w":
                            Node(str(y+2) + str(x+2) + str(y+1) + str(x+1), parent=root)

                if y + 1 < ROWS and x - 1 >= 0:
                    if board.squares[y+1][x-1].piece is None:
                        Node(str(y+1) + str(x-1), parent=root)
                    elif y + 2 < ROWS and x - 2 >= 0:
                        if board.squares[y+2][x-2].piece is None and board.squares[y+1][x-1].piece.team == "w":
                            Node(str(y+2) + str(x-2) + str(y+1) + str(x-1), parent=root)

            print(RenderTree(root))
            return [node.name for node in PreOrderIter(root)]
        
    def chaining(self, y, x, board):
        chains=[]
        fronta=[]
        fronta.append(str(y) + str(x))
        while fronta:
            y = int(fronta[0][0])
            x = int(fronta[0][1])
            print(str(x) + str(y))
            if self.team == "w":
                if y - 2 >= 0 and x + 2 < COLS and board.squares[y-1][x+1].piece is not None:
                    print("b")
                    if board.squares[y-2][x+2].piece is None and board.squares[y-1][x+1].piece.team == "b":
                        chains.append(str(y-2) + str(x+2))
                        fronta.append(str(y-2) + str(x+2))

                if y - 2 >= 0 and x - 2 >= 0 and board.squares[y-1][x-1].piece is not None:
                    print("a")
                    if board.squares[y-2][x-2].piece is None and board.squares[y-1][x-1].piece.team == "b":
                        chains.append(str(y-2) + str(x-2))
                        fronta.append(str(y-2) + str(x-2))

            fronta.pop(0)
            
        print("chains: " + str(chains))
