import pygame
import math
from checkers.constants import SQUARE_SIZE, WIDTH, HEIGHT, YELLOW, BLACK, DARK_YELLOW
from checkers.board import Board
 
FPS = 60
 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")
board = Board()
 
def main():
    selected_piece = False
    run = True
    clock = pygame.time.Clock()
 
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
 
                if selected_piece == True:
                    if board.squares[y][x].piece is not None:
                        board.squares[y][x].piece.color = board.squares[y][x].piece.default_color     
                        prev_y = y
                        prev_x = x
                        x, y = get_mouse_pos()
                        if board.squares[y][x].piece is None and board.squares[y][x].color == YELLOW or board.squares[y][x].color == DARK_YELLOW:
                            if board.squares[y][x].color == DARK_YELLOW:
                                color_squares(prev_y, prev_x, BLACK)
                                despawn(prev_y, prev_x, str(y) + str(x))
                                board.squares[y][x].piece = board.squares[prev_y][prev_x].piece
                                color_squares(y, x, DARK_YELLOW)
                                board.squares[y][x].piece.color = YELLOW
                                board.squares[prev_y][prev_x].piece = None
                                break
                            color_squares(prev_y, prev_x, BLACK)
                            despawn(prev_y, prev_x, str(y) + str(x))
                            board.squares[y][x].piece = board.squares[prev_y][prev_x].piece
                            board.squares[prev_y][prev_x].piece = None
                            board.squares[y][x].piece.color = board.squares[y][x].piece.default_color
                            selected_piece = False
                            break
                        else:
                            color_squares(prev_y, prev_x, BLACK)
 
                x, y = get_mouse_pos()
                if board.squares[y][x].piece is not None:
                    board.squares[y][x].piece.color = YELLOW
                    selected_piece = True
                    color_squares(y, x, DARK_YELLOW)
 
        board.draw_board(WIN)
        pygame.display.update()
 
    pygame.quit()
 
def get_mouse_pos():
    x, y = pygame.mouse.get_pos()
    x = math.floor(x / SQUARE_SIZE)
    y = math.floor(y / SQUARE_SIZE)
    return x, y
 
def color_squares(y, x, color):
    l = 0
    for pos in board.squares[y][x].piece.get_possible_moves(y, x, board, None, end_check = False):
        i = int(pos[0])
        j = int(pos[1])
        if y != i and x != j:
            board.squares[i][j].color = color
 
    for pos in board.squares[y][x].piece.get_possible_moves(y, x, board, None, end_check = True):
        color2 = YELLOW
        if color == BLACK:
            color2 = BLACK
        if l == 0:
            l = 1
        else:
            i = int(pos[0])
            j = int(pos[1])
            board.squares[i][j].color = color2    
 
def despawn(prev_y, prev_x, pos_despawning):
    board.despawn_piece(board.squares[prev_y][prev_x].piece.get_possible_moves(prev_y, prev_x, board, pos_despawning, False))
 
if __name__ == "__main__":
    main()