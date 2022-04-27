import pygame
import math
from checkers.constants import SQUARE_SIZE, WIDTH, HEIGHT
from checkers.board import Board

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")
board = Board()

def main():
    run = True
    clock = pygame.time.Clock()
    board.create_board()

    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x = math.floor(x / SQUARE_SIZE)
                y = math.floor(y / SQUARE_SIZE)
                board_click(x, y)

        board.draw_board(WIN)
        pygame.display.update()

    pygame.quit()

def board_click(x, y):
    print(y, x)
    print(board.squares[y][x].piece)

if __name__ == "__main__":
    main()