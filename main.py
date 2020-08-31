import pygame
import threading
from solver import solve, check_viable_numbers

pygame.init()
pygame.font.init()


class Box:
    WIDTH = 60

    def __init__(self, xcord, ycord):
        self.xcord = xcord
        self.ycord = ycord
        self.number = None
        self.viable_numbers = set()
        self.block = False

    def draw(self, screen, font):
        if self.number is not None:
            number_surface = font.render(f"{self.number}", False, (0, 0, 0))
            x = self.xcord * self.WIDTH + 0.5 * self.WIDTH - 0.5 * number_surface.get_width()
            y = self.ycord * self.WIDTH + 0.5 * self.WIDTH - 0.5 * number_surface.get_height()
            screen.blit(number_surface, (int(x), int(y)))

    def change_number(self, x, board):
        if x is None:
            self.block = False
            self.number = x
        else:
            if x in check_viable_numbers(self, board):
                self.block = True
                self.number = x

SIZE = (9 * Box.WIDTH, 9 * Box.WIDTH)
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Sudoku Solver")
FONT = pygame.font.SysFont('Comic Sans MS', 30)


def create_sudoku_board(rows=9):
    board = []
    for _ in range(rows):
        board.append([])
    for x in range(rows):
        for y in range(rows):
            board[x].append(Box(x, y))
    return board


def draw_grid(screen, rows=9, width=Box.WIDTH):
    GREY = (121, 121, 121)
    BLACK = (0, 0, 0)
    screen.fill((255, 255, 255))
    for col in range(rows):
        if col % 3 != 0:
            pygame.draw.line(screen, GREY, (width * col, 0), (width * col, rows * width + width))
            pygame.draw.line(screen, GREY, (0, width * col), (rows * width + width, width * col))
        else:
            pygame.draw.line(screen, BLACK, (width * col, 0), (width * col, rows * width + width), 4)
            pygame.draw.line(screen, BLACK, (0, width * col), (rows * width + width, width * col), 4)


def get_Box_mouse(width, board):
    mx, my = pygame.mouse.get_pos()
    if 0 <= mx <= SIZE[0] and 0 <= my <= SIZE[1]:
        x = mx // width
        y = my // width
        return board[x][y]
    else:
        return None


def draw_numbers(screen, board, font):
    for row in board:
        for box in row:
            box.draw(screen, font)


def draw_selected(screen, box):
    ORANGE = (255, 150, 0)
    if box is not None:
        pygame.draw.rect(screen, ORANGE, (box.xcord * box.WIDTH, box.ycord * box.WIDTH, box.WIDTH, box.WIDTH), 4)


def get_pressed_key(event):
    if event.key == pygame.K_1:
        return 1
    elif event.key == pygame.K_2:
        return 2
    elif event.key == pygame.K_3:
        return 3
    elif event.key == pygame.K_4:
        return 4
    elif event.key == pygame.K_5:
        return 5
    elif event.key == pygame.K_6:
        return 6
    elif event.key == pygame.K_7:
        return 7
    elif event.key == pygame.K_8:
        return 8
    elif event.key == pygame.K_9:
        return 9

def mainloop():
    run = True
    solving = [False, False] # [solving, solved]
    selected_box = None
    solve_thread = None
    board = create_sudoku_board()

    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not solving[0]:
                selected_box = get_Box_mouse(Box.WIDTH, board)
            elif event.type == pygame.KEYDOWN and not solving[0]:
                if event.key != pygame.K_SPACE and event.key != pygame.K_r:
                    selected_box.change_number(get_pressed_key(event), board)
                elif event.key == pygame.K_SPACE and not solving[1]:
                    solving[0] = True
                    solve_thread = threading.Thread(target=solve, args=(board,solving))
                    solve_thread.start()
                elif event.key == pygame.K_r:
                    # RESET
                    solving = [False, False]
                    selected_box = None
                    solve_thread = None
                    board = create_sudoku_board()
        draw_grid(SCREEN)
        draw_selected(SCREEN, selected_box)
        draw_numbers(SCREEN, board, FONT)
        pygame.display.update()


mainloop()
