import pygame
import base_func, board, generator, eval

def run():
    WIDTH, HEIGHT = 400, 400
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess board")

    START_POSSITION = "rnbkqbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBKQBNR"
    FPS = 30
    chess_board = board.Board(START_POSSITION, WIDTH, HEIGHT, SCREEN)
    moveGenerationObj = generator.MovesGenerator(chess_board)
    moves_counter = 0
    running = True
    all_moves_made = list()
    are_moves_generated = False
    clicked_squares = list()

    while running:
        chess_board.Draw_Board()
        if len(clicked_squares) > 0: 
            chess_board.Draw_Legal_Moves(moves, clicked_squares[0])
        chess_board.Draw_Pieces()
        if are_moves_generated == False:
            chess_board.Pawn_promotion()
            moves = moveGenerationObj.Generate_legal_moves(all_moves_made, True, 1 if moves_counter % 2 == 0 else -1)
            are_moves_generated = True
            if moves == 'Checkmate':
                running = False
                print("Checkmate!")

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
                        chess_board.Set_clicked_piece(clicked_squares[0])
                    else:
                        clicked_squares = list()
                        chess_board.Reset_clicked_piece()
                elif len(clicked_squares) == 2:
                    if clicked_squares[0] != clicked_squares[1]:
                        content_square = chess_board.Check_square(clicked_squares[1])
                        if content_square == 'Empty':
                            if moveGenerationObj.CheckIfMoveIsInGeneratedMoves(clicked_squares[0], clicked_squares[1]):
                                chess_board.Make_a_move(clicked_squares)
                                moves_counter +=1
                                all_moves_made.append(clicked_squares)
                                are_moves_generated = False
                        else:
                            if chess_board.Are_pieces_diff_color(clicked_squares):
                                if moveGenerationObj.CheckIfMoveIsInGeneratedMoves(clicked_squares[0], clicked_squares[1]):
                                    chess_board.Make_a_move(clicked_squares)
                                    moves_counter +=1
                                    all_moves_made.append(clicked_squares)
                                    are_moves_generated = False
                    chess_board.Reset_clicked_piece()
                    clicked_squares = list()
            pygame.display.update()
            clock.tick(FPS)
    print("Your game took: " + str(int(moves_counter/2)) + " moves!")

if __name__ == '__main__':
    run()
