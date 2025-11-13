import pygame

std_y = 1400
std_x = std_y
FPS = 60
doble_kill = False
skip = False

# - - Pygame - -
pygame.init()
screen = pygame.display.set_mode((std_y, std_x))
pygame.display.set_caption("Шашки")
font = pygame.font.SysFont("arial", 22)
clock = pygame.time.Clock()

tab = 100
board_x_std = 8
board_y_std = board_x_std
line_checkers_std = 3
board_size = std_y - 2 * tab
size = board_size / board_x_std
size_k_checker = 3
size_k_var = 5
width_r = 16
width_c = 6

black_board = (80, 40, 20)
white_board = (230, 230, 170)
white = (255, 255, 230)
black = (0, 0, 0)
grey_black = (80, 80, 80)
grey_white = (160, 180, 180)
green = (80, 250, 50)
dark_green = (50, 130, 50)

kommand_step = 'white'
var = []
var_step = []

def draw_crown(surface, center, radius, color=(255, 215, 0)):

    x, y = center
    # масштаб под радиус
    crown_width = radius * 1.2
    crown_height = radius * 0.8
    top = y - crown_height / 2
    bottom = y + crown_height / 2

    # точки трёх зубцов
    points = [
        (x - crown_width / 2, bottom),                 # левый низ
        (x - crown_width / 3, top),                    # левый зубец
        (x, bottom - crown_height * 0.65),             # центральный пик
        (x + crown_width / 3, top),                    # правый зубец
        (x + crown_width / 2, bottom),                 # правый низ
    ]

    # сам контур короны
    pygame.draw.polygon(surface, color, points)
    # обводка для чёткости
    pygame.draw.lines(surface, (0, 0, 0), True, points, 2)


def if_kill(board, i, j):

    checker = board[i][j]
    kill_var = []
    for n in (-1, 1):

        if check_board_super(n + i, 1 + j, board, checker.color, n * 2 + i, 2 + j):
            kill_var.append(VarStep(n * 2 + i, 2 + j, checker, (n + i, 1 + j)))

        if check_board_super(n + i, -1 + j, board, checker.color, n * 2 + i, -2 + j):
            kill_var.append(VarStep(n * 2 + i, -2 + j, checker, (n + i, -1 + j)))

    return kill_var

def draw_board(board) -> None:

    for i in range(len(board)):
        for j in range(len(board[0])):

            color = (black_board, white_board)[int((j + i) % 2 == 0)]
            pygame.draw.rect(screen, color,
                             (j * size + tab, i * size + tab, size, size))

            if board[i][j] is not None:
                board[i][j].draw(screen)

    pygame.draw.rect(screen, white,
                     (tab - width_r, tab - width_r,
                      board_size + width_r * 2, board_size + width_r * 2), width=width_r)


def check_board(y, x, board):
    if 0 <= y < board_y_std and 0 <= x < board_x_std and board[y][x] is None:
        return True
    return False


def check_board_super(y, x, board, color_step, y2, x2):
    if (0 <= y < board_y_std and 0 <= x < board_x_std and 0 <= x2 < board_x_std and 0 <= y2 < board_y_std
            and board[y][x] is not None):
        if board[y][x].color is not None and board[y][x].color != color_step:
            if board[y2][x2] is None:
                return True
    return False

def cenrt_x_y(x, y):
    return x * size + tab + size / 2, y * size + tab + size / 2


class VarStep:

    def __init__(self, x, y, checker, kill_step=None):
        self.x = x
        self.y = y
        self.size = size / size_k_var
        self.checker = checker
        self.kill_step = kill_step

    def draw(self, screen_b, color=green):
        cx_v, cy_v = cenrt_x_y(self.x, self.y)
        pygame.draw.circle(screen_b, color, (cy_v, cx_v), self.size)


class Checker:

    def __init__(self, color, y, x):
        self.color = color          # 'white' или 'black'
        self.y = y
        self.x = x
        self.king = False        # станет True при достижении края
        self.size = size / size_k_checker


    def draw(self, surface):
        # вычисляем координаты центра
        cx, cy = cenrt_x_y(self.x, self.y)
        color = white if self.color == 'white' else black
        outline = grey_white if self.color == 'white' else grey_black

        pygame.draw.circle(surface, color, (cx, cy), self.size)
        pygame.draw.circle(surface, outline, (cx, cy), self.size, width=width_c)

        if self.king:
            draw_crown(surface, (cx, cy), self.size)


    def if_king(self):
        if self.y == 0 and self.color == 'white' or self.color == 'black' and self.y == board_y_std - 1:
            self.king = True


class Board:

    def __init__(self, board_x, board_y, line_checkers):
        self.board = []
        for i in range(line_checkers):
            self.board.append([Checker('black', i, j) if (i + j) % 2 != 0 else None for j in range(board_x)])

        for i in range(board_y - 2 * line_checkers):
            self.board.append([None for _ in range(board_x)])

        for i in range(line_checkers):
            row = board_y - line_checkers + i
            self.board.append([Checker('white', row, j) if (row + j) % 2 != 0 else None for j in range(board_x)])

    def step_var(self, i, j, kommand): # координаты обьекта и команда, которая сейчас ходит.
        checker = self.board[i][j]

        if checker is None or checker.color != kommand:
            pass

        else:
            var.clear()

            if not checker.king:

                if kommand == 'black': step_y = 1
                else: step_y = -1

                if check_board(step_y + i, 1 + j, self.board):
                    var.append(VarStep(step_y + i, 1 + j, checker))

                if check_board(step_y + i, -1 + j, self.board):
                    var.append(VarStep(step_y + i, -1 + j, checker))

            else:

                for step_y in (-1, 1):

                    if check_board(step_y + i, 1 + j, self.board):
                        var.append(VarStep(step_y + i, 1 + j, checker))

                    if check_board(step_y + i, -1 + j, self.board):
                        var.append(VarStep(step_y + i, -1 + j, checker))

            for dop_var in if_kill(self.board, i, j):
                var.append(dop_var)

        return var

    def step(self, old_pos, new_pos):

        k = False
        if self.board[old_pos[0]][old_pos[1]].king:
            k = True
        self.board[old_pos[0]][old_pos[1]] = None
        self.board[new_pos[0]][new_pos[1]] = Checker(kommand_step, new_pos[0], new_pos[1])
        self.board[new_pos[0]][new_pos[1]].king = k
        self.board[new_pos[0]][new_pos[1]].if_king()

b1 = Board(board_x_std, board_y_std, line_checkers_std)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    clock.tick(FPS)
    draw_board(b1.board)
    pygame.display.flip()

    mx, my = pygame.mouse.get_pos()

    if not doble_kill:
        for i in b1.board:
            for j in i:
                if j is not None:
                    cx, cy = cenrt_x_y(j.x, j.y)
                    if (mx - cx) ** 2 + (my - cy) ** 2 < (size / size_k_checker) ** 2:
                        var_step = b1.step_var(j.y, j.x, kommand_step)

    if skip:
        skip = False
        var_step.clear()

    for h in var_step:
        h.draw(screen)

        cy, cx = cenrt_x_y(h.x, h.y)
        if (mx - cx) ** 2 + (my - cy) ** 2 < (size / size_k_var) ** 2:
            h.draw(screen, dark_green)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:

                    b1.step((h.checker.y, h.checker.x), (h.x, h.y))

                    if h.kill_step is not None:

                        b1.board[h.kill_step[0]][h.kill_step[1]] = None
                        q =  if_kill(b1.board, h.x, h.y)

                        if len(q) > 0:
                            var_step = q
                            doble_kill = True
                            q = ()
                            break

                        else:
                            doble_kill = False
                            q = ()
                            var_step = []
                            skip = True
                            kommand_step = 'black' if kommand_step == 'white' else 'white'
                            break

                    var_step.clear()
                    kommand_step = 'black' if kommand_step == 'white' else 'white'

        if skip: break


    pygame.display.flip()

