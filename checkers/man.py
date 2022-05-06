import pygame
from .piece import Piece
from anytree import Node, RenderTree, PreOrderIter

class Man(Piece):
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val):
        self._color = val

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

    def get_possible_moves(self, pos):
        #Zalozeni stromu ->
        a = Node(pos)
        #Logika (for) - pokud ano, tak ->
        #b = Node("A6", parent=a) #last_charac = chr(ord(last_charac) + 1)
        #return [node.name for node in PreOrderIter(1)]