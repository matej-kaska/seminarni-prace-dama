import pygame
import math
import random
from tkinter import *
from checkers.constants import AQUA, CRIMSON, SQUARE_SIZE, WIDTH, HEIGHT, YELLOW, BLACK, DARK_YELLOW, ROWS, COLS, WHITE, RED, GREEN
from checkers.board import Board
from checkers.man import Man
from checkers.king import King
from checkers.render import export_render
from checkers.csv_handler import CSV_Handler
from checkers.button import Button
 
FPS = 60 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Checkers")

board = Board()
load_btn = Button(WHITE, YELLOW, 850, 50, 100, 50, "LOAD")
save_btn = Button(WHITE, YELLOW, 850, 150, 100, 50, "SAVE")
debug_btn = Button(WHITE, YELLOW, 850, 250, 100, 50, "DEBUG")
restart_btn = Button(WHITE, YELLOW, 850, 450, 100, 50, "RESTART")
checkbox_btn = Button(RED, YELLOW, 850, 550, 100, 50, "Red is bot")
buttons = [load_btn, save_btn, debug_btn, restart_btn, checkbox_btn]
csv_handler = CSV_Handler()

render = ""
debug = False
turn_count = 0
tie_turn_count = 0
kill_check = False
prev_white_pos = []
prev_black_pos = []
red_is_bot = False
 
def main():
    selected_piece = False
    turn = "w"
    turn_counter("reset")
    tie_turn_counter("reset")
    kill_checker("false")
    analyze = ""
    debug_open = False
    run = True
    clock = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.SysFont("inkfree", 26, bold=True)
    turn_label_black = font.render("XXXXXXXXXXXX", True, BLACK, BLACK)
    turn_label = font.render("Blue's Turn", True, AQUA, BLACK)
    turn_rect = turn_label.get_rect()
    turn_rect.center = ((WIDTH - 800) / 2 + 800, 375)
    WIN.blit(turn_label, turn_rect)
    board_analyze("win_detection", "", "", "")
    while run:
        clock.tick(FPS)
        if debug == True:
            if debug_open == False:
                debug_open = True
                win_debug = Tk()
                win_debug.geometry("400x400")
                win_debug.overrideredirect(True)
                label_render = Label(win_debug, text=export_render(), font=("Helvetica 14 bold"), justify=LEFT)
                win_debug.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if selected_piece == True:
                    if x < COLS and board.squares[y][x].piece is not None:
                        board.squares[y][x].piece.color = board.squares[y][x].piece.default_color     
                        prev_y = y
                        prev_x = x
                        x, y = get_mouse_pos()
                        if x < COLS and board.squares[y][x].piece is None and board.squares[y][x].color == YELLOW or x < COLS and board.squares[y][x].color == DARK_YELLOW:
                            if board.squares[y][x].color == DARK_YELLOW:
                                color_squares(prev_y, prev_x, BLACK)
                                despawn(prev_y, prev_x, str(y) + str(x), False)
                                board.squares[y][x].piece = board.squares[prev_y][prev_x].piece
                                board.squares[prev_y][prev_x].piece = None
                                color_squares(y, x, DARK_YELLOW)
                                board.squares[y][x].piece.color = YELLOW
                                if debug == True:
                                    debug_render(win_debug, label_render)
                                break
                            color_squares(prev_y, prev_x, BLACK)
                            despawn(prev_y, prev_x, str(y) + str(x), True)
                            board.squares[y][x].piece = board.squares[prev_y][prev_x].piece
                            board.squares[prev_y][prev_x].piece = None
                            board.squares[y][x].piece.color = board.squares[y][x].piece.default_color
                            selected_piece = False
                            king_spawn_check(y, x)
                            if board.squares[y][x].piece.team == "w":
                                turn = "b"
                            else:
                                turn = "w"
                            analyze = board_analyze("win_detection", turn, prev_white_pos, prev_black_pos)
                            break
                        else:
                            color_squares(prev_y, prev_x, BLACK)
                        
                x, y = get_mouse_pos()
                menu_buttons()
                if x < COLS and board.squares[y][x].piece is not None and board.squares[y][x].piece.team == turn:
                    possible_moves = board_analyze("possible_moves", turn, prev_white_pos, prev_black_pos)
                    if str(y) + str(x) in possible_moves:
                        board.squares[y][x].piece.color = YELLOW
                        selected_piece = True
                        color_squares(y, x, DARK_YELLOW)
                    if debug == True:
                        debug_render(win_debug, label_render)
            elif event.type == pygame.MOUSEMOTION:
                highlight_buttons()

        if red_is_bot == True and turn == "b" and analyze != "white_win" and analyze != "black_win":
            turn_label = font.render("Red's Turn", True, CRIMSON, BLACK)
            renderer(turn_label_black, turn_label, turn_rect, ((WIDTH - 800) / 2 + 800, 375))
            possible_moves = board_analyze("possible_moves", turn, prev_white_pos, prev_black_pos)
            if possible_moves != []:
                bot_piece = random.choice(possible_moves)
                bot_y = int(bot_piece[0])
                bot_x = int(bot_piece[1])
                pos = color_squares(bot_y, bot_x, DARK_YELLOW)
                pos = random.choice(pos)
                bot_next_y = int(pos[0])
                bot_next_x = int(pos[1])
                color_squares(bot_y, bot_x, BLACK)
                despawn(bot_y, bot_x, str(bot_next_y) + str(bot_next_x), True)
                board.squares[bot_next_y][bot_next_x].piece = board.squares[bot_y][bot_x].piece
                board.squares[bot_y][bot_x].piece = None
                board.squares[bot_next_y][bot_next_x].piece.color = board.squares[bot_next_y][bot_next_x].piece.default_color
                king_spawn_check(bot_next_y, bot_next_x)
                turn = "w"
            analyze = board_analyze("win_detection", turn, prev_white_pos, prev_black_pos)
        
        board.draw_board(WIN)
        for btn in buttons:
            btn.draw(WIN)
        if turn == "w":
            turn_label = font.render("Blue's Turn", True, AQUA, BLACK)
            renderer(turn_label_black, turn_label, turn_rect, ((WIDTH - 800) / 2 + 800, 375))
        else:
            turn_label = font.render("Red's Turn", True, CRIMSON, BLACK)
            renderer(turn_label_black, turn_label, turn_rect, ((WIDTH - 800) / 2 + 800, 375))
        
        if analyze == "white_win" or analyze == "black_win":
            turn = "x"
            if analyze == "white_win":
                turn_label = font.render("Blue won", True, AQUA, BLACK)
                renderer(turn_label_black, turn_label, turn_rect, ((WIDTH - 800) / 2 + 800, 375))
            if analyze == "black_win":
                turn_label = font.render("Red won", True, CRIMSON, BLACK)
                renderer(turn_label_black, turn_label, turn_rect, ((WIDTH - 800) / 2 + 800, 375))

        if analyze == "tie":
            turn = "x"
            turn_label = font.render("Tie", True, WHITE, BLACK)
            renderer(turn_label_black, turn_label, turn_rect, ((WIDTH - 800) / 2 + 800, 375))
        pygame.display.update()
 
    pygame.quit()
 
def get_mouse_pos():
    x, y = pygame.mouse.get_pos()
    x = math.floor(x / SQUARE_SIZE)
    y = math.floor(y / SQUARE_SIZE)
    return x, y

def menu_buttons():
    pos = pygame.mouse.get_pos()
    for btn in buttons:
        if btn.is_over(pos):
            if btn.text == "LOAD":
                csv_handler.load_from_csv(board)
                main()
                return
            elif btn.text == "SAVE":
                csv_handler.save_to_csv(board)
                return
            elif btn.text == "DEBUG":
                global debug
                debug = True
                return
            elif btn.text == "RESTART":
                board.restart_board()
                main()
                return
            elif btn.text == "Red is bot":
                global red_is_bot
                if btn.default_color == RED:
                    btn.color = GREEN
                    btn.default_color = btn.color
                    red_is_bot = TRUE
                    return
                else:
                    btn.color = RED
                    btn.default_color = btn.color
                    red_is_bot = FALSE
                    return
                
def highlight_buttons():
    pos = pygame.mouse.get_pos()
    for btn in buttons:
        if btn.is_over(pos) and btn.text != "Red is bot":
            btn.color = btn.highlight_color
        else:
            btn.color = btn.default_color
 
def color_squares(y, x, color):
    end_pos = []
    for pos in board.squares[y][x].piece.get_possible_moves(y, x, board, None, end_check = False, analyze = False):
        i = int(pos[0])
        j = int(pos[1])
        if y != i and x != j:
            board.squares[i][j].color = color
    for pos in board.squares[y][x].piece.get_possible_moves(y, x, board, None, end_check = True, analyze = False)[1:]:
        color2 = YELLOW
        if color == BLACK:
            color2 = BLACK
        i = int(pos[0])
        j = int(pos[1])
        board.squares[i][j].color = color2
        end_pos.append(pos)
    if red_is_bot == True:
        return end_pos

def despawn(prev_y, prev_x, pos_despawning, end):
    board.despawn_piece(board.squares[prev_y][prev_x].piece.get_possible_moves(prev_y, prev_x, board, pos_despawning, end, analyze = False))

def king_spawn_check(y, x):
    if y == 0 and type(board.squares[y][x].piece) == Man and board.squares[y][x].piece.color == AQUA:
        board.spawn_king(y, x)
    if y == ROWS - 1 and type(board.squares[y][x].piece) == Man and board.squares[y][x].piece.color == CRIMSON:
        board.spawn_king(y, x)

def debug_render(win_debug, label_render):
    label_render.config(text=export_render())
    label_render.pack()
    win_debug.update()

def board_analyze(analyzer, turn, prev_white_pos, prev_black_pos):
    font_warn = pygame.font.SysFont("inkfree", 16)
    warn_label = font_warn.render('', True, BLACK, BLACK)
    warn_rect = warn_label.get_rect()
    warn_rect.center = ((WIDTH - 800) / 2 + 800, 405)
    warn_label_black = font_warn.render("XXXXXXXXXXXXXXXXXXXXXXXXXX", True, BLACK, BLACK)
    if analyzer == "win_detection":
        white_count = 0
        black_count = 0
        playable = True
        raw_possible_moves = []
        white_pos = []
        black_pos = []
        
        for i in range(ROWS):
            for j in range(COLS):
                if board.squares[i][j].piece is not None:
                    if board.squares[i][j].piece.team == "w":
                        white_count = white_count + 1
                        if type(board.squares[i][j].piece) == Man:
                            white_pos.append(str(i) + str(j))
                    else:
                        black_count = black_count + 1
                        if type(board.squares[i][j].piece) == Man:
                            black_pos.append(str(i) + str(j))

        if kill_check == False:
            if white_pos == prev_white_pos and black_pos == prev_black_pos:
                turn_counter("add")
            else:
                turn_counter("reset")
            if (white_count <= 2 and black_count == 1) or (black_count <= 2 and white_count == 1):
                tie_turn_counter("add")
            else:
                tie_turn_counter("reset")
        else:
            turn_counter("reset")
            tie_turn_counter("reset")
            kill_checker("false")

        pos_saver(white_pos, black_pos)

        if tie_turn_count > 0:
            warn_label = font_warn.render("capture in " + str(5-tie_turn_count) + " turns or tie", True, WHITE, BLACK)
            renderer(warn_label_black, warn_label, warn_rect, ((WIDTH - 800) / 2 + 800, 405))
        elif turn_count > 0:
            warn_label = font_warn.render("capture in " + str(15-turn_count) + " turns or tie", True, WHITE, BLACK)
            renderer(warn_label_black, warn_label, warn_rect, ((WIDTH - 800) / 2 + 800, 405))
        else:
            renderer(warn_label_black, warn_label_black, warn_rect, ((WIDTH - 800) / 2 + 800, 405))

        if turn_count >= 15 or tie_turn_count >= 5:
            renderer(warn_label_black, warn_label_black, warn_rect, ((WIDTH - 800) / 2 + 800, 405))
            return "tie"
        if white_count == 0:
            return "black_win"
        if black_count == 0:
            return "white_win"

        for i in range(ROWS):
            for j in range(COLS):
                if board.squares[i][j].piece is not None:
                    if board.squares[i][j].piece.team == turn:
                        raw_possible_moves.append(board.squares[i][j].piece.get_possible_moves(i, j, board, None, end_check = True, analyze = True))

        for pos in raw_possible_moves:
            pos.pop(0)
            if len(pos) >= 1:
                playable = True
                break
            else:
                playable = False
        if playable == False:
            return "tie"

    if analyzer == "possible_moves":
        possible_moves = []
        raw_possible_moves = []
        possible_kills = []
        for i in range(ROWS):
            for j in range(COLS):
                if board.squares[i][j].piece is not None:
                    if board.squares[i][j].piece.team == turn:
                        raw_possible_moves.append(board.squares[i][j].piece.get_possible_moves(i, j, board, None, end_check = True, analyze = True))
        for pos in raw_possible_moves:
            if len(pos) > 1:
                possible_moves.append(pos[0])
                if len(pos) >= 2:
                    for pos2 in pos:
                        if len(pos2) > 2:
                            possible_kills.append(pos[0])
        if len(possible_kills) >= 1:
            kingkill = False
            for pos in possible_kills:
                if type(board.squares[int(pos[0])][int(pos[1])].piece) == King:
                    if kingkill == False:
                        possible_kills = []
                        kingkill = True
                    possible_kills.append(str(pos[0]) + str(pos[1]))
            kill_checker("true")
            return possible_kills
        else:
            return possible_moves

def turn_counter(function):
    global turn_count
    if function == "add":
        turn_count = turn_count + 1
    if function == "reset":
        turn_count = 0
    return turn_count

def tie_turn_counter(function):
    global tie_turn_count
    if function == "add":
        tie_turn_count = tie_turn_count + 1
    if function == "reset":
        tie_turn_count = 0
    return tie_turn_count

def kill_checker(function):
    global kill_check
    if function == "true":
        kill_check = True
    if function == "false":
        kill_check = False
    return kill_check

def pos_saver(white, black):
    global prev_white_pos
    global prev_black_pos
    prev_white_pos = white
    prev_black_pos = black

def renderer(label_black, label, rect, pos):
    WIN.blit(label_black, rect)
    rect = label.get_rect()
    rect.center = pos
    WIN.blit(label, rect)

if __name__ == "__main__":
    main()