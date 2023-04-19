import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

GRID_SIZE = 100
ROWS = HEIGHT // GRID_SIZE
COLS = WIDTH // GRID_SIZE

MINE_COUNT = 10
game_start_time = pygame.time.get_ticks()

COLORS = {
    1: (0, 0, 255),     # Blue
    2: (0, 128, 0),     # Green
    3: (255, 0, 0),     # Red
    4: (0, 0, 128),     # Dark Blue
    5: (128, 0, 0),     # Maroon
    6: (0, 128, 128),   # Teal
    7: (0, 0, 0),       # Black
    8: (128, 128, 128)  # Gray
}
BOMB_COLOR = (200, 0, 0)  # Red
HOVER_COLOR = (200, 200, 200)
PRESSED_COLOR = (150, 150, 150)


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_mine = False
        self.adjacent_mines = 0
        self.is_revealed = False
        self.is_flagged = False
        self.is_hovered = False
        self.is_pressed = False

    def reveal(self):
        self.is_revealed = True

    def toggle_flag(self):
        self.is_flagged = not self.is_flagged

def generate_board(rows, cols, mine_count, first_click_row, first_click_col):
    # Create an empty board
    board = [[Cell(row, col) for col in range(cols)] for row in range(rows)]

    # Randomly place mines
    mines_placed = 0
    while mines_placed < mine_count:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        if not board[row][col].is_mine and not (abs(row - first_click_row) <= 1 and abs(col - first_click_col) <= 1):
            board[row][col].is_mine = True
            mines_placed += 1

    # Calculate adjacent mine counts for each cell
    for row in range(rows):
        for col in range(cols):
            if not board[row][col].is_mine:
                adjacent_mines = 0
                for r in range(-1, 2):
                    for c in range(-1, 2):
                        if 0 <= row + r < rows and 0 <= col + c < cols and board[row + r][col + c].is_mine:
                            adjacent_mines += 1
                board[row][col].adjacent_mines = adjacent_mines

    return board

def reveal_mines(board):
    for row in range(ROWS):
        for col in range(COLS):
            cell = board[row][col]
            if cell.is_mine:
                cell.reveal()


def check_win(board):
    for row in range(ROWS):
        for col in range(COLS):
            cell = board[row][col]
            if not cell.is_mine and not cell.is_revealed:
                return False
    return True

def handle_input(board, event, game_over, first_click):
    elapsed_time = pygame.time.get_ticks() - game_start_time
    if elapsed_time < 500:
        return

    col, row = pygame.mouse.get_pos()
    row, col = row // GRID_SIZE, col // GRID_SIZE

    if 0 <= row < ROWS and 0 <= col < COLS:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left-click
                board[row][col].is_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            row, col = event.pos[1] // GRID_SIZE, event.pos[0] // GRID_SIZE

            if first_click[0]:
                first_click[0] = False
                board[:] = generate_board(ROWS, COLS, MINE_COUNT, row, col)
            
            cell = board[row][col]
            if event.button == 1:  # Left-click
                if not cell.is_flagged:
                    if cell.is_mine:
                        reveal_mines(board)
                        game_over[0] = True
                        print("You lost!")
                    elif cell.adjacent_mines == 0:
                        reveal_adjacent_cells(board, row, col)
                    else:
                        cell.reveal()
            elif event.button == 3:  # Right-click
                cell.toggle_flag()

        elif event.type == pygame.MOUSEMOTION:
            for r in range(ROWS):
                for c in range(COLS):
                    board[r][c].is_hovered = (r == row and c == col)
    else:
        for r in range(ROWS):
            for c in range(COLS):
                board[r][c].is_hovered = False




def reveal_adjacent_cells(board, row, col):
    if not (0 <= row < ROWS) or not (0 <= col < COLS):
        return

    cell = board[row][col]
    if cell.is_revealed or cell.is_mine:
        return

    cell.reveal()

    if cell.adjacent_mines == 0:
        for r in range(-1, 2):
            for c in range(-1, 2):
                reveal_adjacent_cells(board, row + r, col + c)


def draw_board(board, win):
    win.fill(WHITE)

    for row in range(ROWS):
        for col in range(COLS):
            cell = board[row][col]
            rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)

            if cell.is_revealed:
                pygame.draw.rect(win, GRAY, rect)
                if cell.is_mine:
                    pygame.draw.circle(win, BOMB_COLOR, rect.center, GRID_SIZE // 4)
                elif cell.adjacent_mines > 0:
                    font = pygame.font.SysFont('comicsansms', GRID_SIZE - 20)
                    text = font.render(str(cell.adjacent_mines), True, COLORS[cell.adjacent_mines])
                    win.blit(text, rect.move(GRID_SIZE // 4, GRID_SIZE // 4 - 30))
            else:
                if cell.is_hovered and not cell.is_pressed:
                    pygame.draw.rect(win, HOVER_COLOR, rect)
                elif cell.is_pressed:
                    pygame.draw.rect(win, PRESSED_COLOR, rect)
                else:
                    pygame.draw.rect(win, WHITE, rect)

                pygame.draw.rect(win, BLACK, rect, 1)

                if cell.is_flagged:
                    pygame.draw.circle(win, BLACK, rect.center, GRID_SIZE // 4)

    pygame.display.update()


def main():
    empty_board = [[Cell(row, col) for col in range(COLS)] for row in range(ROWS)]
    board = empty_board.copy()

    running = True
    game_over = [False]
    first_click = [True]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                handle_input(board, event, game_over, first_click)

            if check_win(board):
                print("You won!")
                game_over[0] = True
                pygame.quit()

        draw_board(board, WIN)

    pygame.quit()




if __name__ == "__main__":
    main()
