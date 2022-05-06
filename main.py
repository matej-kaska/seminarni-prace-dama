import pygame
import math
from checkers.constants import SQUARE_SIZE, WIDTH, HEIGHT, YELLOW
from checkers.board import Board

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")
board = Board()

def main():
    selected = False
    run = True
    clock = pygame.time.Clock()
    board.create_board()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if selected == True:
                    if board.squares[y][x].piece is not None:
                        board.squares[y][x].piece.color = board.squares[y][x].piece.default_color
                        BeforeY = y
                        BeforeX = x
                        x, y = pygame.mouse.get_pos()
                        x = math.floor(x / SQUARE_SIZE)
                        y = math.floor(y / SQUARE_SIZE)
                        if board.squares[y][x].piece is None:
                            board.squares[y][x].piece = board.squares[BeforeY][BeforeX].piece
                            board.squares[BeforeY][BeforeX].piece = None
                            board.squares[y][x].piece._color = board.squares[y][x].piece.default_color
                            selected = False
                            break

                x, y = pygame.mouse.get_pos()
                x = math.floor(x / SQUARE_SIZE)
                y = math.floor(y / SQUARE_SIZE)
                board_click(x, y)
                if board.squares[y][x].piece is not None:
                    board.squares[y][x].piece.color = YELLOW
                    selected = True
        board.draw_board(WIN)
        pygame.display.update()

    pygame.quit()

def board_click(x, y):
    print(y, x)
    print(board.squares[y][x].label)

if __name__ == "__main__":
    main()