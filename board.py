import os
import pygame
from base_func import Square_to_position, Compare_pieces_colour

class Board():
    def __init__(self, start_position, sqr_size, screen):
        self.white = (255, 255, 255)
        self.black = (181, 101, 29)
        self.red = (255,0,0)
        self.screen = screen
        self.sqr_size = sqr_size
        self.pieces = [''] * 64 # CONTENT IN ORDER: piece_type, path_to_img, position_x, position_y
        self.checked_square = -10

        #### INIT THE STARTING POSITION
        self.startPos = start_position
        id = 0
        path = os.path.dirname(os.path.abspath(__file__))
        for piece in self.startPos:
                if(piece != '/'):
                    if(piece.isdigit()):
                        id += int(piece)
                    else:
                        self.pieces[id] = [
                                    piece, 
                                    pygame.image.load(r"{}\{}\{}.png".format
                                    (path, 'White' if piece.islower() else 'Black' ,piece.lower())), 
                                    Square_to_position(id, self.sqr_size)]
                        id += 1

    def Draw_Board(self,height, width):
        self.screen.fill(self.black)
        for y in range(0, height, self.sqr_size):
            for x in range(0, width, self.sqr_size*2):
                if y % int(width/4) != 0:
                    pygame.draw.rect(self.screen, self.white, (x + self.sqr_size, y, self.sqr_size, self.sqr_size))
                else:
                    pygame.draw.rect(self.screen, self.white, (x, y, self.sqr_size, self.sqr_size))
        if self.checked_square != -10:
            x,y =Square_to_position(self.checked_square, self.sqr_size)
            pygame.draw.rect(self.screen, self.red, (x,y , self.sqr_size, self.sqr_size))

    def Draw_Pieces(self):
        for piece in self.pieces:
            if(piece != ''):
                self.screen.blit(pygame.transform.scale(piece[1], (self.sqr_size,self.sqr_size)), 
                                    Square_to_position(self.pieces.index(piece), self.sqr_size)
                                )

    def Draw_Legal_Moves(self, legal_moves, piece_sqr):
        for piece_moves in legal_moves:
            if(piece_moves[0] == piece_sqr):
                for move in piece_moves[1]:
                    x,y = Square_to_position(move, self.sqr_size)
                    pygame.draw.circle(self.screen, (255,0,0), (x + 25, y + 25), 10)

    def Make_a_move(self, sqrs):
        self.pieces[sqrs[1]] = self.pieces[sqrs[0]]
        self.pieces[sqrs[0]] = ''
    
    def Check_square(self, square):
        if self.pieces[square] == '':
            return 'Empty'
        elif self.pieces[square][0].isupper():
            return 'Black'
        return 'White'

    def Are_pieces_diff_color(self, sqrs):
        return Compare_pieces_colour(sqrs[0], sqrs[1], self.pieces)

    def Get_pos(self):
        return self.pieces
    
    def Change_checked_king_square(self,sqr):
        self.checked_square = sqr