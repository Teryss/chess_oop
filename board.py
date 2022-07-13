import os
import pygame
import time
from base_func import Square_to_position, Compare_pieces_colour, Position_to_square

class Board():
    def __init__(self, start_position, sqr_size, screen):
        self.white = (255, 255, 255)
        self.black = (181, 101, 29)
        self.red = (255,0,0)
        self.screen = screen
        self.sqr_size = sqr_size
        self.pieces = [''] * 64 # CONTENT IN ORDER: piece_type, path_to_img, position_x, position_y
        self.checked_square = -10
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.drawPromotion = False

        #### INIT THE STARTING POSITION
        self.startPos = start_position
        id = 0
        for piece in self.startPos:
                if(piece != '/'):
                    if(piece.isdigit()):
                        id += int(piece)
                    else:
                        self.pieces[id] = [
                                    piece, 
                                    pygame.image.load(r"{}\{}\{}.png".format
                                    (self.path, 'White' if piece.islower() else 'Black' ,piece.lower())), 
                                    Square_to_position(id, self.sqr_size)]
                        id += 1
        ### GET PROMOTION PIECES
        self.promotion_pieces_imgs = {
            'r' : pygame.image.load(r"{}\{}\{}.png".format(self.path, 'White','r')),
            'R' : pygame.image.load(r"{}\{}\{}.png".format(self.path, 'Black','R')),
            'b' : pygame.image.load(r"{}\{}\{}.png".format(self.path, 'White','b')),
            'B' : pygame.image.load(r"{}\{}\{}.png".format(self.path, 'Black','B')),
            'n' : pygame.image.load(r"{}\{}\{}.png".format(self.path, 'White','n')),
            'N' : pygame.image.load(r"{}\{}\{}.png".format(self.path, 'Black','N')),
            'q' : pygame.image.load(r"{}\{}\{}.png".format(self.path, 'White','q')),
            'Q' : pygame.image.load(r"{}\{}\{}.png".format(self.path, 'Black','Q')),
        }

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

    def Pawn_promotion(self):
        squares_to_check = [x for x in range(0,8)] + [x for x in range(56,64)] 
        
        for i in squares_to_check:
            if self.pieces[i] != '':
                if self.pieces[i][0] == 'p' or self.pieces[i][0] == 'P':
                    print("Promotion")
                    pawn_type = self.pieces[i][0]
                    pygame.draw.rect(self.screen, (0,0,0), (self.sqr_size * 2, self.sqr_size * 4, self.sqr_size * 4, self.sqr_size * 1))
                    self.screen.blit(pygame.transform.scale(self.promotion_pieces_imgs['q'], (self.sqr_size,self.sqr_size)), (self.sqr_size * 2, self.sqr_size * 4))
                    self.screen.blit(pygame.transform.scale(self.promotion_pieces_imgs['b'], (self.sqr_size,self.sqr_size)), (self.sqr_size * 3, self.sqr_size * 4))
                    self.screen.blit(pygame.transform.scale(self.promotion_pieces_imgs['n'], (self.sqr_size,self.sqr_size)), (self.sqr_size * 4, self.sqr_size * 4))
                    self.screen.blit(pygame.transform.scale(self.promotion_pieces_imgs['r'], (self.sqr_size,self.sqr_size)), (self.sqr_size * 5, self.sqr_size * 4))
                    pygame.display.update()
                    sqr = 0
                    while sqr == 0:
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                sqr = Position_to_square( pygame.mouse.get_pos() )
                                piece_type = ''
                                #34 - q, 35 b , 36 n , 37 r
                                if sqr == 34:
                                    piece_type = 'q'
                                elif sqr == 35:
                                    piece_type = 'b'
                                elif sqr == 36:
                                    piece_type = 'n'
                                elif sqr == 37:
                                    piece_type = 'r'
                                else:
                                    sqr = 0
                                    break
                                if pawn_type.isupper():
                                    piece_type = piece_type.upper()

                                self.pieces[i] = [
                                    piece_type,
                                    pygame.image.load(r"{}\{}\{}.png".format
                                                    (self.path, 'White' if piece_type.islower() else 'Black' ,piece_type.lower())),
                                                    self.pieces[i][2]
                                ]

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
