import pygame
from anytree import Node, RenderTree, PreOrderIter

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

    def get_possible_moves(self, pos):
        #Zalozeni stromu ->
        a = Node(pos)
        #Logika (for) - pokud ano, tak ->
        #b = Node("A6", parent=a) #last_charac = chr(ord(last_charac) + 1)
        #return [node.name for node in PreOrderIter(1)]