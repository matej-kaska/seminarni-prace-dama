from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, color):
        self._color = color
        self._default_color = color

    @abstractmethod
    def get_possible_moves(self):
        pass

    @abstractmethod
    def draw_piece(self):
        pass