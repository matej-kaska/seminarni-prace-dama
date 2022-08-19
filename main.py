import pygame
import math
from tkinter import *
from checkers.constants import AQUA, CRIMSON, SQUARE_SIZE, WIDTH, HEIGHT, YELLOW, BLACK, DARK_YELLOW, ROWS, COLS, WHITE
from checkers.board import Board
from checkers.man import Man
from checkers.render import export_render
 
FPS = 60
 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")
board = Board()
render = ""
debug = False
 
def main():
    selected_piece = False
    turn = "w"
    debug_open = False
    run = True
    clock = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.SysFont("inkfree", 26)
    font.bold = True
    turn_label_black = font.render('XXXXXXXXXXXX', True, BLACK, BLACK)
    turn_label = font.render('Blue Turns', True, AQUA, BLACK)
    turn_rect = turn_label.get_rect()
    turn_rect.center = ((WIDTH - 800) / 2 + 800, 375)
    WIN.blit(turn_label, turn_rect)
    while run:
        clock.tick(FPS)
        if debug == True:
            if debug_open == False:
                debug_open = True
                win_debug = Tk()
                win_debug.title("Dáma - debug")
                win_debug.geometry("400x400")
                win_debug.overrideredirect(True)
                label_render = Label(win_debug, text=export_render(), font=('Helvetica 14 bold'), justify=LEFT)
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
                                color_squares(y, x, DARK_YELLOW)
                                board.squares[y][x].piece.color = YELLOW
                                board.squares[prev_y][prev_x].piece = None
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
                            break
                        else:
                            color_squares(prev_y, prev_x, BLACK)
                        
                x, y = get_mouse_pos()
                if x < COLS and board.squares[y][x].piece is not None and board.squares[y][x].piece.team == turn:
                    board.squares[y][x].piece.color = YELLOW
                    selected_piece = True
                    color_squares(y, x, DARK_YELLOW)
                    if debug == True:
                        debug_render(win_debug, label_render)
        board.draw_board(WIN)
        draw_menu()
        if turn == "w":
            WIN.blit(turn_label_black, turn_rect)
            turn_label = font.render('Blue Turns', True, AQUA, BLACK)
            WIN.blit(turn_label, turn_rect)
        else:
            WIN.blit(turn_label_black, turn_rect)
            turn_label = font.render('Red Turns', True, CRIMSON, BLACK)
            WIN.blit(turn_label, turn_rect)
        pygame.display.update()
 
    pygame.quit()
 
def get_mouse_pos():
    x, y = pygame.mouse.get_pos()
    x = math.floor(x / SQUARE_SIZE)
    y = math.floor(y / SQUARE_SIZE)
    return x, y
 
def color_squares(y, x, color):
    for pos in board.squares[y][x].piece.get_possible_moves(y, x, board, None, end_check = False):
        i = int(pos[0])
        j = int(pos[1])
        if y != i and x != j:
            board.squares[i][j].color = color
    for pos in board.squares[y][x].piece.get_possible_moves(y, x, board, None, end_check = True)[1:]:
        color2 = YELLOW
        if color == BLACK:
            color2 = BLACK
        i = int(pos[0])
        j = int(pos[1])
        board.squares[i][j].color = color2
        
def despawn(prev_y, prev_x, pos_despawning, end):
    board.despawn_piece(board.squares[prev_y][prev_x].piece.get_possible_moves(prev_y, prev_x, board, pos_despawning, end))

def king_spawn_check(y, x):
    if y == 0 and type(board.squares[y][x].piece) == Man and board.squares[y][x].piece.color == AQUA:
        board.spawn_king(y, x)
    if y == ROWS - 1 and type(board.squares[y][x].piece) == Man and board.squares[y][x].piece.color == CRIMSON:
        board.spawn_king(y, x)

def text_objects(text, font):
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()

def button(msg, x, y, width, height, inactive_color, active_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(WIN, active_color, (x, y, width, height))

        if click[0] == 1:
            if msg == "LOAD":
                board.add_pieces_from_csv()
                return
            elif msg == "SAVE":
                board.save_game()
                return
            elif msg == "DEBUG":
                global debug
                debug = True
                return
    else:
        pygame.draw.rect(WIN, inactive_color, (x, y, width, height))

    font = pygame.font.SysFont("inkfree", 16)
    text_surf, text_rect = text_objects(msg, font)
    text_rect.center = ((x + width/2), (y + height/2))
    WIN.blit(text_surf, text_rect)

def draw_menu():
    button("LOAD", 850, 50, 100, 50, WHITE, YELLOW)
    button("SAVE", 850, 150, 100, 50, WHITE, YELLOW)
    button("DEBUG", 850, 250, 100, 50, WHITE, YELLOW)

def debug_render(win_debug, label_render):
    label_render.config(text=export_render())
    label_render.pack()
    win_debug.update()

if __name__ == "__main__":
    main()