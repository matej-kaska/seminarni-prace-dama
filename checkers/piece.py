import pygame
from .constants import BLUE, RED
from anytree import Node, PreOrderIter

class Piece:
    def __init__(self, color):
        self._color = color
        self._defaultColor = color

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
        root = None
        root = Node(str(y) + str(x))
        #Logika (for) - pokud ano, tak ->
        if board.squares[y][x].piece is not None:
            if self._defaultColor == BLUE:
                if x + 1 < 8:
                    if board.squares[y-1][x+1].piece is None:
                        new = Node(str(y-1) + str(x+1), parent=root)
                if y - 1 > -2:
                    if board.squares[y-1][x-1].piece is None and x-1 >= 0:
                        new = Node(str(y-1) + str(x-1), parent=root)
            if self._defaultColor == RED:
                if x + 1 < 8:
                    if board.squares[y+1][x+1].piece is None:
                        new = Node(str(y+1) + str(x+1), parent=root)
                if y - 1 > -2:
                    if board.squares[y+1][x-1].piece is None and x-1 >= 0:
                        new = Node(str(y+1) + str(x-1), parent=root)
            return [node.name for node in PreOrderIter(root)]