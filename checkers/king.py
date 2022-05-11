import pygame
from .piece import Piece
from .constants import CORAL

class King(Piece):
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
        pygame.draw.ellipse(
            win,
            CORAL,
            (square.x * square.size + square.size / 5,
            square.y * square.size + square.size / 5,
            square.size / 5 * 3,
            square.size / 5 * 3), 3
            )

    def get_possible_moves(self):
        ...