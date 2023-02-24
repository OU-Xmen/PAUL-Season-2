try:
    import pygame
    pygame.init()
    import os
    import sys
    import time
    import random
    import ChessBoard as B
    import ChessPiece as CP
    maindirectory = os.path.dirname(os.path.abspath(__file__))
    assetdirectory = os.path.join(maindirectory, 'assets')
except ImportError:
    print("One or more modules failed to load")
    quit()

def main():
    # create 800x600 window
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Chess')
    icon = pygame.image.load(os.path.join(assetdirectory, 'icon32.png'))
    pygame.display.set_icon(icon)

    game_board = B.Board()
    legal_moves_flag = False
    made_move = []
    whose_turn = 0 # start with white

    while True: # game loop
        mouse = pygame.mouse.get_pos()
        mouse_ij = ((mouse[1]-60)//60, (mouse[0]-60)//60)
        mouse_on_board = mouse_ij[0] in range(8) and mouse_ij[1] in range(8)

        screen.fill("black")
        game_board.draw_board(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_on_board and game_board.board[mouse_ij[0]][mouse_ij[1]].id and game_board.board[mouse_ij[0]][mouse_ij[1]].color == ('white','black')[whose_turn]:
                    if game_board.board[mouse_ij[0]][mouse_ij[1]].id == "P":
                        made_move = game_board.clicked_on(mouse_ij[0], mouse_ij[1], screen)
                    else:
                        made_move = game_board.clicked_on(mouse_ij[0], mouse_ij[1], screen)
                    if made_move:
                        whose_turn = 1 - whose_turn
                else:
                    print("No")

        pygame.display.flip()

        break_flag = False
        winner = game_board.game_is_over()
        if winner:
            print(f"{winner} wins!")
            break_flag = True
        if break_flag: break

if __name__ == "__main__": main()