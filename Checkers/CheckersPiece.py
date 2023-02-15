import pygame, os
pygame.init()
maindirectory = os.path.dirname(os.path.abspath(__file__))
assetdirectory = os.path.join(maindirectory, 'assets')

class Checker():
    def __init__(self, color, x, y, alive = True):
        self.alive = alive
        self.king_switch = False
        if color == 0: # 0: black piece; 1: red piece; -1: empty
            self.color = 'black'
            self.color_num = 0
            self.piece = pygame.image.load(os.path.join(assetdirectory, 'black_piece.png'))
        elif color == 1:
            self.color = 'red'
            self.color_num = 1
            self.piece = pygame.image.load(os.path.join(assetdirectory, 'red_piece.png'))
        elif color == -1:
            self.color = None
            self.color_num = -1
            self.piece = pygame.image.load(os.path.join(assetdirectory, 'icon32.png'))
        self.x = x
        self.y = y
        self.list_x = (x-60)//60
        self.list_y = (y-60)//60

    def duplicate(self):
        return self.color_num, self.x, self.y

    def set_life(self, alive):
        self.alive = alive
    
    def get_life(self):
        return self.alive
    
    def set_king(self, king_switch):
        self.king_switch = king_switch
    
    def get_king(self):
        return self.king_switch

    def set_color(self, color):
        if color == 0: # 0: black piece, 1: red piece
            self.color = 'black'
            self.color_num = 0
            self.piece = pygame.image.load(os.path.join(assetdirectory, 'black_piece.png'))
        elif color == 1:
            self.color = 'red'
            self.color_num = 1
            self.piece = pygame.image.load(os.path.join(assetdirectory, 'red_piece.png'))
        else:
            self.color = None
            self.color_num = -1
            self.piece = pygame.image.load(os.path.join(assetdirectory, 'icon32.png'))
    
    def get_color(self):
        return self.color if self.color else False

    def get_color_num(self):
        return self.color_num
    
    def draw_piece(self, screen):
        if self.alive:
            screen.blit(self.piece, (self.x, self.y))
        else:
            pygame.draw.rect(screen,(170, 110, 20), (self.x, self.y, 60, 60))

    def clicked_on(self, screen, board, new_color, new_king):
        # when this piece is clicked, legal moves for the piece
        # will be highlighted, as well as multiple jumps. if a
        # legal move is clicked, the piece will play that move. if
        # anywhere else is clicked, the piece will be deselected.

        # self is board[self.list_y][self.list_x] == True

        legal_moves = self.get_legal_moves(board)
        if len(legal_moves) == 0: return

        while True: # piece selected loop
            mouse = pygame.mouse.get_pos()
            mouse_tile = ((mouse[1]-60)//60, (mouse[0]-60)//60)
            break_flag = False

            for x, y in legal_moves:
                pygame.draw.rect(screen, (220, 170, 60), (60*(1+y), 60*(1+x), 60, 60))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse_tile in legal_moves:
                        # set new spot with same attributes as selection piece
                        board[mouse_tile[0]][mouse_tile[1]].set_life(True)
                        board[mouse_tile[0]][mouse_tile[1]].set_color(new_color)
                        if board[self.list_y][self.list_x].get_king(): # retain king status
                            board[mouse_tile[1]][mouse_tile[0]].set_king(True)
                            board[self.list_y][self.list_x].set_king(False)
                        
                        if abs(mouse_tile[0] - self.list_x) > 1:
                            # set spot jumped over to empty
                            board[int((self.list_x + mouse_tile[0])/2)][int((self.list_y + mouse_tile[1])/2)].set_life(False)
                            board[int((self.list_x + mouse_tile[0])/2)][int((self.list_y + mouse_tile[1])/2)].set_color(-1)

                        # set old spot to empty
                        board[self.list_x][self.list_y].set_life(False)
                        board[self.list_x][self.list_y].set_color(-1)

                        # set king_switch when blackpiece.list_x == 0
                        if (mouse_tile[0] == 7*new_color):
                            board[mouse_tile[1]][mouse_tile[0]].set_king(True)
                        return True
                    return False
            
            if break_flag:
                break
        return

    def get_legal_moves(self, jacob: list[list[int]]):
        # use self.x, self.y to see vacant spots in such diagonal patterns:
        # Key: _ = vacant, X = occupied, [B, R] = [black, red]
        # B_
        # BR_
        # BR_[R_]...
        # after one non-jump, the turn is over
        # after one jump, legal jumps must be found from the spot the piece has
        # landed on, excluding the jump it just made

        legal_moves = []
        
        for mx, my in [(-2,2), (-2,-2), (2,-2), (2,2)]: # find legal single jumps
            in_bounds = (self.list_x + mx) in range(8) and (self.list_y + my) in range(8) and jacob[self.list_x + mx][self.list_y + my].get_color_num() == -1
            new_me = jacob[self.list_x][self.list_y]
            if in_bounds:
                jumping_over = jacob[int(self.list_x + (mx/2))][int(self.list_y + (my/2))].get_color_num() == 1 - new_me.get_color_num()
            forward_direction = 2*new_me.get_color_num() - 1
            forward_move = forward_direction == int(mx/2)

            if (self.get_king() or forward_move) and in_bounds and jumping_over and (not jacob[self.list_x + mx][self.list_y + my].get_life()):
                legal_moves.append((self.list_x + mx, self.list_y + my))

        if not legal_moves:
            for mx, my in [(-1,1), (-1,-1), (1,-1), (1,1)]: # find legal non-jumps
                in_bounds = (self.list_x + mx) in range(8) and (self.list_y + my) in range(8)
                new_me = jacob[self.list_x][self.list_y]
                forward_direction = 2*new_me.get_color_num() - 1
                forward_move = forward_direction == mx
                
                if (self.get_king() or forward_move) and in_bounds and (not jacob[self.list_x + mx][self.list_y + my].get_life()):
                    legal_moves.append((self.list_x + mx, self.list_y + my))

        return legal_moves