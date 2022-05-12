import pygame
from .piece import Piece
from .constants import COLS, ROWS, CORAL
from anytree import Node, RenderTree, search

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

    def get_possible_moves(self, y, x, board, despawning, end_check):
        despawn_check = 0
        rightup_node = 0
        leftup_node = 0
        leftdown_node = 0
        rightdown_node = 0
        root = Node(str(y) + str(x))
        root2 = Node(str(y) + str(x))

        if board.squares[y][x].piece is not None:
            next_y = y
            next_x = x
            check_rightup = True
            check_rightdown = False
            check_leftdown = False
            check_leftup = False
            move_cycling = True

            # Basic moves (without kill)

            while move_cycling == True:
                if next_y - 1 >= 0 and next_x + 1 < COLS and check_rightup == True:
                    if board.squares[next_y-1][next_x+1].piece is None:
                        rightup_node = rightup_node + 1

                if next_y - 1 >= 0 and next_x - 1 >= 0 and check_leftup == True:
                    if board.squares[next_y-1][next_x-1].piece is None:
                        leftup_node = leftup_node + 1

                if next_y + 1 < ROWS and next_x - 1 >= 0 and check_leftdown == True:
                    if board.squares[next_y+1][next_x-1].piece is None:
                        leftdown_node = leftdown_node + 1

                if next_y + 1 < ROWS and next_x + 1 < COLS and check_rightdown == True:
                    if board.squares[next_y+1][next_x+1].piece is None:
                        rightdown_node = rightdown_node + 1
                
                if next_y >= 0 and check_rightdown == True:
                    next_y = next_y + 1
                    next_x = next_x + 1
                    if next_y == ROWS + 1:
                        check_rightdown = False
                        move_cycling = False
                
                if next_y <= ROWS and check_leftdown == True:
                    next_y = next_y + 1
                    next_x = next_x - 1
                    if next_y == ROWS + 1:
                        next_y = y
                        next_x = x
                        check_leftdown = False
                        check_rightdown = True
                
                if next_y <= ROWS and check_leftup == True:
                    next_y = next_y - 1
                    next_x = next_x - 1
                    if next_y == -1:
                        next_y = y
                        next_x = x
                        check_leftup = False
                        check_leftdown = True

                if next_y >= 0 and check_rightup == True:
                    next_y = next_y - 1
                    next_x = next_x + 1
                    if next_y == -1:
                        next_y = y
                        next_x = x
                        check_rightup = False
                        check_leftup = True

            print("leftup: " + str(leftup_node))
            print("leftdown: " + str(leftdown_node))
            print("rightup: " + str(rightup_node))
            print("rightdown: " + str(rightdown_node))
