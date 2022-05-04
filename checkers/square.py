import pygame
from .constants import SQUARE_SIZE

class Square:
    def __init__(self, x, y, color):
        self._x = x
        self._y = y
        self._color = color
        self._size = SQUARE_SIZE
        self._piece = None
        self._selected = False
        self._label = None

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y  

    @property
    def size(self):
        return self._size

    @property
    def piece(self):
        return self._piece

    @piece.setter
    def piece(self, val):
        self._piece = val
        
    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, val):
        self._selected = val

    @property
    def label(self):
        return self._label
    
    @label.setter
    def label(self, val):
        self._label = val

    @property
    def color(self):
        return self._color

    def draw_square(self, win):
        pygame.draw.rect(win, self._color, (self._x * self._size, self._y * self._size, self._size, self._size))

        if (self._piece is not None):
            self._piece.draw_piece(self, win)