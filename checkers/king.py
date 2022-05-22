import pygame
from .piece import Piece
from .constants import COLS, ROWS, CORAL
from .render import import_render
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
        kills = []

        if board.squares[y][x].piece is not None:
            root, rightup_node, leftup_node, leftdown_node, rightdown_node, kills = self.__move_check(board, y, x, root, root2, rightup_node, leftup_node, leftdown_node, rightdown_node, kills)
            next_y = y
            next_x = x
            
            # Prodloužení políček pokud je to možné (po chainingu)

            if root.is_leaf == False:
                possible_end_moves_more = []
                end_pos = self.__moves_substring(root, possible_end_moves_more, despawn_check, possible_end_moves_more, True)
                for pos in end_pos:
                    y = int(pos[5])
                    x = int(pos[6])
                    ky = int(pos[7])
                    kx = int(pos[8])
                    diff_y = 0
                    diff_x = 0
                    diff_y = ky - y
                    diff_x = kx - x

                    if diff_y > 0 and diff_x > 0: #leftup
                        for i in range(1,8):
                            if y - i >= 0 and x - i >= 0:
                                if board.squares[y-i][x-i].piece is None:
                                    Node(str(y-i) + str(x-i) + str(ky) + str(kx), parent=search.find_by_attr(root, pos[0:4]))
                                else:
                                    break
                    if diff_y < 0 and diff_x > 0: #leftdown
                        for i in range(1,8):
                            if y + i < ROWS and x - i >= 0: 
                                if board.squares[y+i][x-i].piece is None:
                                    Node(str(y+i) + str(x-i) + str(ky) + str(kx), parent=search.find_by_attr(root, pos[0:4]))
                                else:
                                    break
                    if diff_y > 0 and diff_x < 0: #rightup
                        for i in range(1,8):
                            if y - i >= 0 and x + i < COLS:
                                if board.squares[y-i][x+i].piece is None:
                                    Node(str(y-i) + str(x+i) + str(ky) + str(kx), parent=search.find_by_attr(root, pos[0:4]))
                                else:
                                    break
                    if diff_y < 0 and diff_x < 0: #rightdown
                        for i in range(1,8):
                            if y + i < ROWS and x + i < COLS:
                                if board.squares[y+i][x+i].piece is None:
                                    Node(str(y+i) + str(x+i) + str(ky) + str(kx), parent=search.find_by_attr(root, pos[0:4]))
                                else:
                                    break

            # Possible moves při braní, ale bez chainingu

            if len(kills) > 0 and root.is_leaf == True:
                for kill in kills:
                    ky = int(kill[0])
                    kx = int(kill[1])
                    diff_y = 0
                    diff_x = 0
                    diff_y = y - ky
                    diff_x = x - kx
                    enemy_spoted = False

                    if diff_y > 0 and diff_x > 0: #leftup
                        for i in range(1,8):
                            if y - i >= 0 and x - i >= 0:
                                if enemy_spoted == True:
                                    if board.squares[y-i][x-i].piece is None:
                                        Node(str(y-i) + str(x-i) + str(ky) + str(kx), parent=root)
                                    else:
                                        break
                                if board.squares[y-i][x-i].piece is not None:
                                    enemy_spoted = True
                    if diff_y < 0 and diff_x > 0: #leftdown
                        for i in range(1,8):
                            if y + i < ROWS and x - i >= 0:
                                if enemy_spoted == True:
                                    if board.squares[y+i][x-i].piece is None:
                                        Node(str(y+i) + str(x-i) + str(ky) + str(kx), parent=root)
                                    else:
                                        break
                                if board.squares[y+i][x-i].piece is not None:
                                    enemy_spoted = True
                    if diff_y > 0 and diff_x < 0: #rightup
                        for i in range(1,8):
                            if y - i >= 0 and x + i < COLS:
                                if enemy_spoted == True:
                                    if board.squares[y-i][x+i].piece is None:
                                        Node(str(y-i) + str(x+i) + str(ky) + str(kx), parent=root)
                                    else:
                                        break
                                if board.squares[y-i][x+i].piece is not None:
                                    enemy_spoted = True
                    if diff_y < 0 and diff_x < 0: #rightdown
                        for i in range(1,8):
                            if y + i < ROWS and x + i < COLS:
                                if enemy_spoted == True:
                                    if board.squares[y+i][x+i].piece is None:
                                        Node(str(y+i) + str(x+i) + str(ky) + str(kx), parent=root)
                                    else:
                                        break
                                if board.squares[y+i][x+i].piece is not None:
                                    enemy_spoted = True

            # Possible moves bez braní

            if root.is_leaf == True:
                for i in range(1, rightup_node + 1):
                    Node(str(next_y-i) + str(next_x+i), parent=root)
                    Node(str(next_y-i) + str(next_x+i), parent=root2)
                for i in range(1, leftup_node + 1):
                    Node(str(next_y-i) + str(next_x-i), parent=root)
                    Node(str(next_y-i) + str(next_x-i), parent=root2)
                for i in range(1, leftdown_node + 1):
                    Node(str(next_y+i) + str(next_x-i), parent=root)
                    Node(str(next_y+i) + str(next_x-i), parent=root2)
                for i in range(1, rightdown_node + 1):
                    Node(str(next_y+i) + str(next_x+i), parent=root)
                    Node(str(next_y+i) + str(next_x+i), parent=root2)
            
            # Possible moves

            possible_moves = []
            despawning = self.__moves_substring(root2, possible_moves, despawn_check, despawning, False)
            
            possible_end_moves = []
            if root.is_leaf == False:
                possible_end_moves.append(str(y) + str(x))
            despawning = self.__moves_substring(root, possible_end_moves, despawn_check, despawning, False)


            if despawning is not None:
                killed = []
                if end_check == True:
                    try:
                        s = str(search.find_by_attr(root, despawning))
                    except:
                        s = str(search.findall_by_attr(root, despawning))
                else:
                    try:
                        s = str(search.find_by_attr(root2, despawning))
                    except:
                        s = str(search.findall_by_attr(root2, despawning))
                for _ in range(s.count("/")):
                    sub = s.find("/")
                    if "/" not in s[sub+1:sub+5]:
                        if ")" not in s[sub+1:sub+5]:
                            killed.append((s[sub+3:sub+5]))
                    s = s[sub+1:] 
                return killed
            if end_check == True:
                import_render(str(RenderTree(root)))
                return possible_end_moves
            else:
                return possible_moves


    def __moves_substring(self, tree_root, arr, despawn_check, despawning, extension):
        s = str(tree_root.leaves)
        for _ in range(s.count("')")):
            sub = s.find("')")
            if (s[sub-3:sub-2]) == "/":
                arr.append(s[sub-2:sub])
            else:
                if extension == True:
                    despawning.append(s[sub-9:sub])
                else:
                    arr.append(s[sub-4:sub-2])
                if despawn_check == 0 and despawning == s[sub-4:sub-2]:
                    despawn_check = 1
                    despawning = despawning + (s[sub-2:sub])
            s = s[sub+1:]
        return despawning

    def __move_check(self, board, y, x, root, root2, rightup_node, leftup_node, leftdown_node, rightdown_node, kills):
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
        
        
        # Move - all directions 
        
        while move_cycling == True:
            if next_y - 1 >= 0 and next_x + 1 < COLS and check_rightup == True:
                if board.squares[next_y-1][next_x+1].piece is None and rightup_blocked == False:
                    rightup_node = rightup_node + 1
                elif rightup_blocked == False:
                    rightup_blocked = True
                    if next_y - 2 >= 0 and next_x + 2 < COLS:
                        if board.squares[next_y-2][next_x+2].piece is None and self.team != board.squares[next_y-1][next_x+1].piece.team:
                            kill_y = next_y - 1
                            kill_x = next_x + 1
                            chain_y = next_y-2
                            chain_x = next_x+2

                            for i in range(7):
                                if next_y - 2 - i >= 0 and next_x + 2 + i < COLS:
                                    if board.squares[next_y-2-i][next_x+2+i].piece is None:
                                        if str(kill_y) + str(kill_x) not in kills:
                                            kills.append(str(kill_y) + str(kill_x))                    
                                            for j in range(7):
                                                if next_y - 2 - i - j >= 0 and next_x + 2 + i + j < COLS or next_y - 2 - i - j == -1 or next_x + 2 + i + j == COLS:
                                                    if next_y - 2 - i - j == -1 or next_x + 2 + i + j == COLS: 
                                                        chain_y = next_y-2-i-j+1
                                                        chain_x = next_x+2+i+j-1
                                                        break
                                                    elif board.squares[next_y-2-i-j][next_x+2+i+j].piece is None:
                                                        chain_y = next_y-2-i-j
                                                        chain_x = next_x+2+i+j
                                                        break
                                        
                                        
                            
                            self.__chaining(str(chain_y) + str(chain_x) + str(kill_y) + str(kill_x), board, root, root2, kills, next_y, next_x)


            if next_y - 1 >= 0 and next_x - 1 >= 0 and check_leftup == True:
                if board.squares[next_y-1][next_x-1].piece is None and leftup_blocked == False:
                    leftup_node = leftup_node + 1
                elif leftup_blocked == False:
                    leftup_blocked = True
                    if next_y - 2 >= 0 and next_x - 2 >= 0:
                        if board.squares[next_y-2][next_x-2].piece is None and self.team != board.squares[next_y-1][next_x-1].piece.team:
                            kill_y = next_y - 1
                            kill_x = next_x - 1
                            chain_y = next_y-2
                            chain_x = next_x-2

                            for i in range(7):
                                if next_y - 2 - i >= 0 and next_x - 2 - i >= 0:
                                    if board.squares[next_y-2-i][next_x-2-i].piece is None:
                                        if str(kill_y) + str(kill_x) not in kills:
                                            kills.append(str(kill_y) + str(kill_x))
                                            for j in range(6):
                                                if next_y - 2 - i - j >= 0 and next_x - 2 - i - j >= 0 or next_y - 2 - i - j == -1 or next_x - 2 - i - j == -1:
                                                    
                                                    if next_y - 2 - i - j == -1 or next_x - 2 - i - j == -1:
                                                        chain_y = next_y-2-i-j-1
                                                        chain_x = next_x-2-i-j-1
                                                        break
                                                    elif board.squares[next_y-2-i-j][next_x-2-i-j].piece is None:
                                                        chain_y = next_y-2-j-i
                                                        chain_x = next_x-2-j-i
                                                        break
                            
                            self.__chaining(str(chain_y) + str(chain_x) + str(kill_y) + str(kill_x), board, root, root2, kills, next_y, next_x)

            if next_y + 1 < ROWS and next_x - 1 >= 0 and check_leftdown == True and leftdown_blocked == False:
                if board.squares[next_y+1][next_x-1].piece is None:
                    leftdown_node = leftdown_node + 1
                elif leftdown_blocked == False:
                    leftdown_blocked = True
                    if next_y + 2 < ROWS and next_x - 2 >= 0:
                        if board.squares[next_y+2][next_x-2].piece is None and self.team != board.squares[next_y+1][next_x-1].piece.team:
                            kill_y = next_y + 1
                            kill_x = next_x - 1
                            chain_y = next_y+2
                            chain_x = next_x-2

                            for i in range(7):
                                if next_y + 2 + i < ROWS and next_x - 2 - i >= 0:
                                    if board.squares[next_y+2+i][next_x-2-i].piece is None:
                                        if str(kill_y) + str(kill_x) not in kills:
                                            kills.append(str(kill_y) + str(kill_x))
                                            for j in range(6):
                                                if next_y + 2 + i + j < ROWS and next_x - 2 - i - j >= 0 or next_y + 2 + i + j == ROWS or next_x - 2 - i - j == -1:
                                                    if next_y + 2 + i + j == ROWS or next_x - 2 - i - j == -1:
                                                        chain_y = next_y+2+i+j+1
                                                        chain_x = next_x-2-i-j-1
                                                        break
                                                    elif board.squares[next_y+2+i+j][next_x-2-i-j].piece is None:
                                                        chain_y = next_y+2+j+i
                                                        chain_x = next_x-2-j-i
                                                        break
                            
                            self.__chaining(str(chain_y) + str(chain_x) + str(kill_y) + str(kill_x), board, root, root2, kills, next_y, next_x)

            if next_y + 1 < ROWS and next_x + 1 < COLS and check_rightdown == True and rightdown_blocked == False:
                if board.squares[next_y+1][next_x+1].piece is None:
                    rightdown_node = rightdown_node + 1
                elif rightdown_blocked == False:
                    rightdown_blocked = True
                    
                    if next_y + 2 < ROWS and next_x + 2 < COLS:
                        if board.squares[next_y+2][next_x+2].piece is None and self.team != board.squares[next_y+1][next_x+1].piece.team:
                            kill_y = next_y + 1
                            kill_x = next_x + 1
                            chain_y = next_y+2
                            chain_x = next_x+2

                            for i in range(7):
                                if next_y + 2 + i < ROWS and next_x + 2 + i < COLS:
                                    if board.squares[next_y+2+i][next_x+2+i].piece is None:
                                        if str(kill_y) + str(kill_x) not in kills:
                                            kills.append(str(kill_y) + str(kill_x))
                                            for j in range(6):
                                                if next_y + 2 + i + j < ROWS and next_x + 2 + i + j < COLS or next_y + 2 + i + j == ROWS or next_x + 2 + i + j == COLS:
                                                    if next_y + 2 + i + j == ROWS or next_x + 2 + i + j == COLS:
                                                        chain_y = next_y+2+i+j+1
                                                        chain_x = next_x+2+i+j+1
                                                        break
                                                    elif board.squares[next_y+2+i+j][next_x+2+i+j].piece is None:
                                                        chain_y = next_y+2+i+j
                                                        chain_x = next_x+2+i+j
                                                        break
                            
                            self.__chaining(str(chain_y) + str(chain_x) + str(kill_y) + str(kill_x), board, root, root2, kills, next_y, next_x)
            
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
                    
        return root, rightup_node, leftup_node, leftdown_node, rightdown_node, kills

    def __chaining(self, pos, board, root, root2, killsc, org_y, org_x):
        fronta = []
        fronta_checked = []
        buffer = pos
        last_buffer = []
        buffer_ru = []
        buffer_lu = []
        buffer_rd = []
        buffer_ld = []
        check_ru = False
        check_lu = False
        check_rd = False
        check_ld = False
        fronta = self.add_fronta(int(pos[0]), int(pos[1]), killsc[0], board, str(org_y) + str(org_x))
        fronta.insert(0, pos + str(org_y) + str(org_x))
        kill_y = killsc[0][0]
        kill_x = killsc[0][1]
        kills = []
        kills.append(killsc[0])
        while fronta:
            
            y = int(fronta[0][0])
            x = int(fronta[0][1])
            next_y = int(fronta[0][0])
            next_x = int(fronta[0][1])
            check_rightup = True
            check_rightdown = False
            check_leftdown = False
            check_leftup = False
            move_cycling = True
            prev_kill_y = fronta[0][2]
            prev_kill_x = fronta[0][3]

            while move_cycling == True:
                if next_y - 1 >= 0 and next_x + 1 < COLS and check_rightup == True:
                    if next_y - 2 >= 0 and next_x + 2 < COLS:
                        if board.squares[next_y-1][next_x+1].piece is not None:
                            if board.squares[next_y-2][next_x+2].piece is None and self.team != board.squares[next_y-1][next_x+1].piece.team:
                                yx = fronta[0][0:2]
                                kill_y = next_y - 1
                                kill_x = next_x + 1
                                killed = self.kill_check(root,str(next_y) + str(next_x) + str(next_y-1) + str(next_x+1), killsc, fronta[0][4:8])

                                if str(kill_y) + str(kill_x) not in killed:
                                    if root.is_leaf == True and check_ru == False:
                                        buffer = str(next_y) + str(next_x) + str(pos[2]) + str(pos[3])
                                        fronta.insert(0, pos + pos)
                                        check_ru = True
                                    else:
                                        if len(fronta[0]) == 6:
                                            if len(buffer) > 2:
                                                if buffer not in str(search.find_by_attr(root, buffer)) and buffer[0:2] not in str(search.find_by_attr(root, buffer[0:2])):
                                                    Node(buffer, parent=root)
                                                Node(str(fronta[0][0:4]), parent=root2)
                                        if len(fronta[0]) != 6:
                                            buffer = fronta[0][4:8]
                                        if fronta[0][0:4] not in str(search.find_by_attr(root, fronta[0][0:4])):
                                            Node(fronta[0][0:4], parent=search.find_by_attr(root, buffer))
                                        last_buffer.append(str(next_y-2) + str(next_x+2) + str(kill_y) + str(kill_x) + fronta[0][0:4])
                                        kills.append(str(kill_y) + str(kill_x))
                                    
                                    if str(next_y-2) + str(next_x+2) not in buffer_ru:
                                        for i in range(7):
                                            if next_y - 2 - i >= 0 and next_x + 2 + i < COLS:
                                                if board.squares[next_y-2-i][next_x+2+i].piece is None:
                                                    if next_y - 3 - i >= 0 and next_x + 3 + i < COLS:
                                                        if board.squares[next_y-3-i][next_x+3+i].piece is not None:
                                                            if board.squares[next_y-3-i][next_x+3+i].piece.team == self.team:
                                                                break
                                                    if str(next_y-2-i) + str(next_x+2+i) + str(kill_y) + str(kill_x) + str(yx) + str(prev_kill_y) + str(prev_kill_x) not in fronta_checked:
                                                        fronta.append(str(next_y-2-i) + str(next_x+2+i) + str(kill_y) + str(kill_x) + str(yx) + str(prev_kill_y) + str(prev_kill_x))
                                        buffer_ru.append(str(next_y-2) + str(next_x+2))
                                            

                if next_y - 1 >= 0 and next_x - 1 >= 0 and check_leftup == True:
                    if next_y - 2 >= 0 and next_x - 2 >= 0:
                        if board.squares[next_y-1][next_x-1].piece is not None:
                            if board.squares[next_y-2][next_x-2].piece is None and self.team != board.squares[next_y-1][next_x-1].piece.team:
                                yx = fronta[0][0:2]
                                kill_y = next_y - 1
                                kill_x = next_x - 1
                                killed = self.kill_check(root,str(next_y) + str(next_x) + str(next_y-1) + str(next_x-1), killsc, fronta[0][4:8])

                                if str(kill_y) + str(kill_x) not in killed:
                                    if root.is_leaf == True and check_lu == False:
                                        buffer = str(next_y) + str(next_x) + str(pos[2]) + str(pos[3])
                                        fronta.insert(0, pos + pos)
                                        check_lu = True
                                    else:
                                        if len(fronta[0]) == 6:
                                            if len(buffer) > 2:
                                                if buffer not in str(search.find_by_attr(root, buffer)) and buffer[0:2] not in str(search.find_by_attr(root, buffer[0:2])):
                                                    Node(buffer, parent=root)
                                                Node(str(fronta[0][0:4]), parent=root2)
                                        if len(fronta[0]) != 6:
                                            buffer = fronta[0][4:8]
                                        if fronta[0][0:4] not in str(search.find_by_attr(root, fronta[0][0:4])):
                                            Node(fronta[0][0:4], parent=search.find_by_attr(root, buffer))
                                        last_buffer.append(str(next_y-2) + str(next_x-2) + str(kill_y) + str(kill_x) + fronta[0][0:4])
                                        kills.append(str(kill_y) + str(kill_x))

                                    if str(next_y-2) + str(next_x-2) not in buffer_lu:
                                        for i in range(7):
                                            if next_y - 2 - i >= 0 and next_x - 2 - i >= 0:
                                                if board.squares[next_y-2-i][next_x-2-i].piece is None:
                                                    if next_y - 3 - i >= 0 and next_x - 3 - i >= 0:
                                                        if board.squares[next_y-3-i][next_x-3-i].piece is not None:
                                                            if board.squares[next_y-3-i][next_x-3-i].piece.team == self.team:
                                                                break
                                                    if str(next_y-2-i) + str(next_x-2-i) + str(kill_y) + str(kill_x) + str(yx) + str(prev_kill_y) + str(prev_kill_x) not in fronta_checked:
                                                        fronta.append(str(next_y-2-i) + str(next_x-2-i) + str(kill_y) + str(kill_x) + str(yx) + str(prev_kill_y) + str(prev_kill_x))
                                        buffer_lu.append(str(next_y-2) + str(next_x-2))

                if next_y + 1 < ROWS and next_x - 1 >= 0 and check_leftdown == True:
                    if next_y + 2 < ROWS and next_x - 2 >= 0:
                        if board.squares[next_y+1][next_x-1].piece is not None:
                            if board.squares[next_y+2][next_x-2].piece is None and self.team != board.squares[next_y+1][next_x-1].piece.team:
                                yx = fronta[0][0:2]
                                kill_y = next_y + 1
                                kill_x = next_x - 1
                                killed = self.kill_check(root, str(next_y) + str(next_x) + str(next_y+1) + str(next_x-1), killsc, fronta[0][4:8])

                                if str(kill_y) + str(kill_x) not in killed:
                                    if root.is_leaf == True and check_ld == False:
                                        buffer = str(next_y) + str(next_x) + str(pos[2]) + str(pos[3])
                                        fronta.insert(0, pos + pos)
                                        check_ld = True
                                    else:
                                        if len(fronta[0]) == 6:
                                            if len(buffer) > 2:
                                                if buffer not in str(search.find_by_attr(root, buffer)) and buffer[0:2] not in str(search.find_by_attr(root, buffer[0:2])):
                                                    Node(buffer, parent=root)
                                                Node(str(fronta[0][0:4]), parent=root2)
                                        if len(fronta[0]) != 6:
                                            buffer = fronta[0][4:8]
                                        if fronta[0][0:4] not in str(search.find_by_attr(root, fronta[0][0:4])):
                                            Node(fronta[0][0:4], parent=search.find_by_attr(root, buffer))
                                        last_buffer.append(str(next_y+2) + str(next_x-2) + str(kill_y) + str(kill_x) + fronta[0][0:4])
                                        kills.append(str(kill_y) + str(kill_x))

                                    if str(next_y+2) + str(next_x-2) not in buffer_ld:
                                        for i in range(7):
                                            if next_y + 2 + i < ROWS and next_x - 2 - i >= 0:
                                                if board.squares[next_y+2+i][next_x-2-i].piece is None:
                                                    if next_y + 3 + i < ROWS and next_x - 3 - i >= 0:
                                                        if board.squares[next_y+3+i][next_x-3-i].piece is not None:
                                                            if board.squares[next_y+3+i][next_x-3-i].piece.team == self.team:
                                                                break
                                                    if str(next_y+2+i) + str(next_x-2-i) + str(kill_y) + str(kill_x) + str(yx) + str(prev_kill_y) + str(prev_kill_x) not in fronta_checked:
                                                        fronta.append(str(next_y+2+i) + str(next_x-2-i) + str(kill_y) + str(kill_x) + str(yx) + str(prev_kill_y) + str(prev_kill_x))
                                        buffer_ld.append(str(next_y+2) + str(next_x-2))

                if next_y + 1 < ROWS and next_x + 1 < COLS and check_rightdown == True:
                    
                    if next_y + 2 < ROWS and next_x + 2 < COLS:
                        if board.squares[next_y+1][next_x+1].piece is not None:
                            if board.squares[next_y+2][next_x+2].piece is None and self.team != board.squares[next_y+1][next_x+1].piece.team:
                                yx = fronta[0][0:2]
                                kill_y = next_y + 1
                                kill_x = next_x + 1
                                killed = self.kill_check(root, str(next_y) + str(next_x) + str(next_y+1) + str(next_x+1), killsc, fronta[0][4:8])
                                if str(kill_y) + str(kill_x) not in killed:
                                    if root.is_leaf == True and check_rd == False:
                                        buffer = str(next_y) + str(next_x) + str(pos[2]) + str(pos[3])
                                        fronta.insert(0, pos + pos)
                                        check_rd = True
                                    else:
                                        if len(fronta[0]) == 6:
                                            if len(buffer) > 2:
                                                if buffer not in str(search.find_by_attr(root, buffer)) and buffer[0:2] not in str(search.find_by_attr(root, buffer[0:2])):
                                                    Node(buffer, parent=root)
                                                Node(str(fronta[0][0:4]), parent=root2)
                                        if len(fronta[0]) != 6:
                                            buffer = fronta[0][4:8]
                                        if fronta[0][0:4] not in str(search.find_by_attr(root, fronta[0][0:4])):
                                            Node(fronta[0][0:4], parent=search.find_by_attr(root, buffer))
                                        last_buffer.append(str(next_y+2) + str(next_x+2) + str(kill_y) + str(kill_x) + fronta[0][0:4])
                                        kills.append(str(kill_y) + str(kill_x))
                                    
                                    if str(next_y+2) + str(next_x+2) not in buffer_rd:
                                        for i in range(7):
                                            if next_y + 2 + i < ROWS and next_x + 2 + i < COLS:
                                                if board.squares[next_y+2+i][next_x+2+i].piece is None:
                                                    if next_y + 3 + i < ROWS and next_x + 3 + i < COLS:
                                                        if board.squares[next_y+3+i][next_x+3+i].piece is not None:
                                                            if board.squares[next_y+3+i][next_x+3+i].piece.team == self.team:
                                                                break
                                                    if str(next_y+2+i) + str(next_x+2+i) + str(kill_y) + str(kill_x) + str(yx) + str(prev_kill_y) + str(prev_kill_x) not in fronta_checked:
                                                        fronta.append(str(next_y+2+i) + str(next_x+2+i) + str(kill_y) + str(kill_x) + str(yx) + str(prev_kill_y) + str(prev_kill_x))
                                        buffer_rd.append(str(next_y+2) + str(next_x+2))

                if next_y >= 0 and check_rightdown == True:
                    next_y = next_y + 1
                    next_x = next_x + 1
                    if next_y == -1 or next_y == 8 or next_x == -1 or next_x == 8:
                        check_rightdown = False
                        move_cycling = False
                
                if next_y <= ROWS and check_leftdown == True:
                    next_y = next_y + 1
                    next_x = next_x - 1
                    if next_y == -1 or next_y == 8 or next_x == -1 or next_x == 8:
                        next_y = y
                        next_x = x
                        check_leftdown = False
                        check_rightdown = True
                
                if next_y <= ROWS and check_leftup == True:
                    next_y = next_y - 1
                    next_x = next_x - 1
                    if next_y == -1 or next_y == 8 or next_x == -1 or next_x == 8:
                        next_y = y
                        next_x = x
                        check_leftup = False
                        check_leftdown = True

                if next_y >= 0 and check_rightup == True:
                    next_y = next_y - 1
                    next_x = next_x + 1
                    if next_y == -1 or next_y == 8 or next_x == -1 or next_x == 8:
                        next_y = y
                        next_x = x
                        check_rightup = False
                        check_leftup = True

            if len(last_buffer) > 0:
                for i in last_buffer:
                    if last_buffer[0][0:4] not in str(search.find_by_attr(root, last_buffer[0][0:4])):
                        killed = self.kill_check(root, last_buffer[0][4:8], killsc, fronta[0][4:8])
                        if last_buffer[0][2:4] not in killed:
                            Node(last_buffer[0][0:4], parent=search.find_by_attr(root, last_buffer[0][4:8]))
                    last_buffer.pop(0)
            fronta_checked.append(fronta[0])
            fronta.pop(0)

    # Přidání pozic do fronty při chainingu
    
    def add_fronta(self, y, x, kills, board, last):
        fronta = []
        ky = int(kills[0])
        kx = int(kills[1])
        diff_y = 0
        diff_x = 0
        diff_y = ky - y
        diff_x = kx - x

        if diff_y > 0 and diff_x > 0: #leftup
            for i in range(1,8):
                if y - i >= 0 and x - i >= 0:
                    if board.squares[y-i][x-i].piece is None:
                        fronta.append(str(y-i) + str(x-i) + str(ky) + str(kx) + last)
                    else:
                        break
        if diff_y < 0 and diff_x > 0: #leftdown
            for i in range(1,8):
                if y + i < ROWS and x - i >= 0:
                    if board.squares[y+i][x-i].piece is None:
                        fronta.append(str(y+i) + str(x-i) + str(ky) + str(kx) + last)
                    else:
                        break
        if diff_y > 0 and diff_x < 0: #rightup
            for i in range(1,8):
                if y - i >= 0 and x + i < COLS:
                    if board.squares[y-i][x+i].piece is None:
                        fronta.append(str(y-i) + str(x+i) + str(ky) + str(kx) + last)
                    else:
                        break
        if diff_y < 0 and diff_x < 0: #rightdown
            for i in range(1,8):
                if y + i < ROWS and x + i < COLS:
                    if board.squares[y+i][x+i].piece is None:
                        fronta.append(str(y+i) + str(x+i) + str(ky) + str(kx) + last)
                    else:
                        break
        return fronta

    # Kontrola killů v chainu

    def kill_check(self, root, pos, kill, f):
        killed = []
        killed.append(kill[0])
        s = str(search.find_by_attr(root, pos))
        if s == "None":
            s = str(search.find_by_attr(root, f))
        for _ in range(s.count("/")):
            sub = s.find("/")
            if "/" not in s[sub+1:sub+5]:
                if ")" not in s[sub+1:sub+5]:
                    if s[sub+3:sub+5] not in killed:
                        killed.append((s[sub+3:sub+5]))
            s = s[sub+1:] 
        return killed