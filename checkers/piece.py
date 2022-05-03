import pygame

class Piece:
    def __init__(self, color, x, y):
        self._color = color
        self._defaultColor = color
        self._draging = False

    def draw_piece(self, square, win):
        pygame.draw.ellipse(
            win,
            self._color,
            (square.x * square.size + square.size / 5,
            square.y * square.size + square.size / 5,
            square.size / 5 * 3,
            square.size / 5 * 3)
            )
    
    