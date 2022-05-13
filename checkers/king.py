from queue import Empty
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
        despawn_check = 1
        rightup_node = 0
        leftup_node = 0
        leftdown_node = 0
        rightdown_node = 0
        root = Node(str(y) + str(x))
        root2 = Node(str(y) + str(x))

        if board.squares[y][x].piece is not None:
            next_y = y
            next_x = x
            rightup_blocked = False
            leftup_blocked = False
            leftdown_blocked = False
            rightdown_blocked = False
            check_rightup = True
            check_rightdown = False
            check_leftdown = False
            check_leftup = False
            move_cycling = True
            killed = []

            
            if killed == []:
            
                # Basic moves (without kill)

                while move_cycling == True:
                    if next_y - 1 >= 0 and next_x + 1 < COLS and check_rightup == True:
                        if board.squares[next_y-1][next_x+1].piece is None and rightup_blocked == False:
                            rightup_node = rightup_node + 1
                            Node(str(next_y-1) + str(next_x+1), parent=root)
                        else:
                            rightup_blocked = True

                    if next_y - 1 >= 0 and next_x - 1 >= 0 and check_leftup == True:
                        if board.squares[next_y-1][next_x-1].piece is None and leftup_blocked == False:
                            leftup_node = leftup_node + 1
                            Node(str(next_y-1) + str(next_x-1), parent=root)
                        else:
                            leftup_blocked = True

                    if next_y + 1 < ROWS and next_x - 1 >= 0 and check_leftdown == True and leftdown_blocked == False:
                        if board.squares[next_y+1][next_x-1].piece is None:
                            leftdown_node = leftdown_node + 1
                            Node(str(next_y+1) + str(next_x-1), parent=root)
                        else:
                            leftdown_blocked = True

                    if next_y + 1 < ROWS and next_x + 1 < COLS and check_rightdown == True and rightdown_blocked == False:
                        if board.squares[next_y+1][next_x+1].piece is None:
                            rightdown_node = rightdown_node + 1
                            Node(str(next_y+1) + str(next_x+1), parent=root)
                        else:
                            rightdown_blocked = True
                    
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
            
            # Possible moves

            possible_end_moves = []
            despawning = self.__moves_substring(root, possible_end_moves, despawn_check, despawning)
            print("leftup: " + str(leftup_node))
            print("leftdown: " + str(leftdown_node))
            print("rightup: " + str(rightup_node))
            print("rightdown: " + str(rightdown_node))
            return possible_end_moves

            

    def __moves_substring(self, tree_root, arr, despawn_check, despawning):
        s = str(tree_root.leaves)
        for _ in range(s.count("')")):
            sub = s.find("')")
            if (s[sub-3:sub-2]) == "/":
                arr.append(s[sub-2:sub])
            else:
                arr.append(s[sub-4:sub-2])
                if despawn_check == 0 and despawning == s[sub-4:sub-2]:
                    despawn_check = 1
                    despawning = despawning + (s[sub-2:sub])
            s = s[sub+1:]
        return despawning
            

            
