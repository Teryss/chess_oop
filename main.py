import pygame
# import sys
# sys.setrecursionlimit(16385)

#Local imports
import base_func, board, generator


width, height = 400, 400
sqr_size = int(width/8)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess board")

startPossition = "rnbkqbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBKQBNR"
fps = 30
chess_board = board.Board(startPossition, sqr_size, screen)
moveGenerationObj = generator.MovesGenerator(chess_board)
moved = True
moves_counter = 0
clicked = False
running = True
all_moves_made = list()
are_moves_generated = False
clicked_squares = list()

while running:
    chess_board.Draw_Board(height, width)
    chess_board.Draw_Pieces()
    if are_moves_generated == False:
        moves = moveGenerationObj.Generate_legal_moves(all_moves_made, get_cur_pos=True)
        are_moves_generated = True
        if moves == 'Checkmate':
            running = False
            print("Checkmate!")
    if len(clicked_squares) > 0: 
        chess_board.Draw_Legal_Moves(moves, clicked_squares[0])

    clock = pygame.time.Clock()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif(event.type == pygame.MOUSEBUTTONDOWN):
            clicked_squares.append( base_func.Position_to_square(pygame.mouse.get_pos()) )
            if len(clicked_squares) == 1:
                content_square = chess_board.Check_square(clicked_squares[0])
                if (content_square == 'Black' and moves_counter % 2 == 1) or (content_square == 'White' and moves_counter % 2 == 0):
                    # print(clicked_squares)
                    continue
                else:
                    clicked_squares = list()
            elif len(clicked_squares) == 2:
                if clicked_squares[0] != clicked_squares[1]:
                    content_square = chess_board.Check_square(clicked_squares[1])
                    if content_square == 'Empty':
                        if moveGenerationObj.CheckIfMoveIsInGeneratedMoves(clicked_squares[0], clicked_squares[1]):
                            chess_board.Make_a_move(clicked_squares)
                            moves_counter +=1
                            all_moves_made.append(clicked_squares[0])
                            are_moves_generated = False
                    else:
                        if chess_board.Are_pieces_diff_color(clicked_squares):
                            if moveGenerationObj.CheckIfMoveIsInGeneratedMoves(clicked_squares[0], clicked_squares[1]):
                                chess_board.Make_a_move(clicked_squares)
                                moves_counter +=1
                                all_moves_made.append(clicked_squares[0])
                                are_moves_generated = False
                clicked_squares = list()
        pygame.display.update()
        clock.tick(fps)
print("Your game took: " + str(int(moves_counter/2)) + " moves!")
