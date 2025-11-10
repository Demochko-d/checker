import pygame
import time

std_y = 1400
std_x = std_y
tab = 100
width_r = 16
width_c = 6

# - - Pygame - -
pygame.init()
screen = pygame.display.set_mode((std_y, std_x))
pygame.display.set_caption("Шашки")
font = pygame.font.SysFont("arial", 22)
clock = pygame.time.Clock()


board_x_std = 8
board_y_std = board_x_std
line_checkers_std = 3
board_size = std_y - 2 * tab
size = board_size / board_x_std


black_board = (80, 40, 20)
white_board = (230, 230, 170)
white = (255, 255, 230)
black = (0, 0, 0)
grey_black = (80, 80, 80)
grey_white = (180, 180, 180)
green = (60, 240, 30)


def draw_board(board: object) -> None:
    for i in range(board_x_std):
        for j in range(board_y_std):

            color = (black_board, white_board)[int((j + i) % 2 == 0)]
            pygame.draw.rect(screen, color,
                             (j * size + tab, i * size + tab, size, size))

            if board[i][j] is not None:
                color, color_g = black, grey_black
                if board[i][j] == 'white': color, color_g = white, grey_white
                pygame.draw.circle(screen, color, (j * size + tab + 0.5 * size, i * size + tab + 0.5 * size),
                                   size / 3)
                pygame.draw.circle(screen, color_g, (j * size + tab + 0.5 * size, i * size + tab + 0.5 * size),
                                   size / 3, width=width_c)

    pygame.draw.rect(screen, white,
                     (tab - width_r, tab - width_r,
                      board_size + width_r * 2, board_size + width_r * 2), width=width_r)


def check_board(y, x, board):
    print(y, x)
    if 0 <= y < board_y_std and 0 <= x < board_x_std and board[y][x] is None:
        return True
    return False


class Checker:

    def __init__(self, color, row, col):
        self.color = color          # 'white' или 'black'
        self.row = row
        self.col = col
        self.king = False           # станет True при достижении края

    def draw(self, surface, size, tab):
        # вычисляем координаты центра
        cx = self.col * size + tab + size / 2
        cy = self.row * size + tab + size /
        # основной цвет
        color = (255, 255, 255) if self.color == 'white' else (0, 0, 0)
        outline = (180, 180, 180) if self.color == 'white' else (60, 60, 60)

        pygame.draw.circle(surface, color, (cx, cy), size / 3)
        pygame.draw.circle(surface, outline, (cx, cy), size / 3, width=6)

        # если дамка — добавим корону
        if self.king:
            pygame.draw.circle(surface, (255, 215, 0), (cx, cy), size / 6)


class Board:

    def __init__(self, board_x, board_y, line_checkers):
        self.board = []
        for i in range(line_checkers):
            self.board.append([Checker('black', i, j) if (i + j) % 2 != 0 else None for j in range(board_x)])

        for i in range(board_y - 2 * line_checkers):
            self.board.append([None for _ in range(board_x)])

        for i in range(line_checkers):
            row = board_y - line_checkers + i
            self.board.append([Checker('white', row, j) if (row + j) % 2 == 0 else None for j in range(board_x)])

    def step_var(self, i, j, kommand): # координаты обьекта и команда, которая сейчас ходит.
        chacker = self.board[i][j]
        var = []
        if chacker != kommand:
            return

        if kommand == 'black': step_y = 1
        else: step_y = -1

        if check_board(step_y + i, 1 + j, self.board):
            var.append((step_y + i, 1 + j))

        if check_board(step_y + i, -1 + j, self.board):
            var.append((step_y + i, -1 + j))


        for h in var:
            pygame.draw.circle(screen, green, (h[1] * size + tab + size * 0.5, h[0] * size + tab + size * 0.5),
                               size / 5)

b1 = Board(board_x_std, board_y_std, line_checkers_std)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    clock.tick(60)
    draw_board(b1)

