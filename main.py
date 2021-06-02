import pygame as p
from game_state import piece
from game_state import game_state
from itertools import chain
import numpy as np
from collections import defaultdict


WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION

BOARD_LIGHT = "bisque4"
BOARD_DARK = "blanchedalmond"
BOARD_HIGHLIGHT = "white"
BOARD_POSSIBLE_MOVE = "brown"


MAX_FPS = 60

IMAGES = {}

pieces_image_reference = {}
    
pieces_image_reference[piece.white | piece.pawn] = 'wp'  
pieces_image_reference[piece.white | piece.rook] = 'wR'  
pieces_image_reference[piece.white | piece.knight] = 'wN' 
pieces_image_reference[piece.white | piece.bishop] = 'wB' 
pieces_image_reference[piece.white | piece.king] = 'wK' 
pieces_image_reference[piece.white | piece.queen] = 'wQ' 

pieces_image_reference[piece.black | piece.pawn] = 'bp' 
pieces_image_reference[piece.black | piece.rook] = 'bR'  
pieces_image_reference[piece.black | piece.knight] = 'bN' 
pieces_image_reference[piece.black | piece.bishop] = 'bB'  
pieces_image_reference[piece.black | piece.king] = 'bK' 
pieces_image_reference[piece.black | piece.queen] = 'bQ' 



def loadImages():

    print("got here")
    

    for piece, sprite in pieces_image_reference.items():
        IMAGES[sprite] = p.transform.scale(p.image.load("images/" + sprite + ".png"), (SQ_SIZE, SQ_SIZE)) 
    
def get_square_under_mouse(board):
    mouse_pos = p.Vector2(p.mouse.get_pos())
    x, y = [int(v // SQ_SIZE) for v in mouse_pos]
    try: 
        if x >= 0 and y >= 0: return (board[y*DIMENSION + x], y*DIMENSION + x)
    except IndexError: pass
    return None, None, None



def main():

    p.init()
    print("inited")
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()

    screen.fill(p.Color("white"))

    curr_state = game_state()
    curr_state.init_classic_board()


    loadImages()
    running = True

    selected_piece = None

    moves = None


    while running:
        
        new_position = get_square_under_mouse(curr_state.board)

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            if e.type == p.MOUSEBUTTONDOWN:
                if not curr_state.turn or (selected_piece and curr_state.turn == (piece.color(selected_piece[0]))) or (new_position[0] >=0 and curr_state.turn == piece.color(new_position[0])):
                    if not selected_piece:
                        
                        if new_position[0] >= 0:
                            selected_piece = new_position
                            moves = curr_state.get_valid_moves(selected_piece)
                            
                            curr_state.board[selected_piece[1]] = -1

                            if not curr_state.turn:
                                curr_state.turn = piece.color(selected_piece[0])


                    elif ((new_position[0] >= 0 and piece.is_enemy(new_position[0], selected_piece[0])) \
                    or curr_state.board[new_position[1]] < 0)\
                    and new_position[1] in moves[1]\
                    or ((piece.rank(selected_piece[0]) in [piece.rook, piece.bishop, piece.queen] and new_position[1] in list(chain.from_iterable(moves[1])))):
                        


                        

                        curr_state.move_piece(selected_piece, new_position)

                        if piece.rank(selected_piece[0]) == piece.pawn:

                            if piece.color(selected_piece[0]) == piece.white:
                                if new_position[1] // DIMENSION == 4:     
                                    curr_state.en_passant = new_position[1]
                                if new_position[1] // DIMENSION == 0:

                                    curr_state.piece_indices[selected_piece[0]].remove(new_position[1])
                                    
                                    selected_piece = (piece.white | piece.queen, selected_piece[1])

                                    curr_state.piece_indices[selected_piece[0]].append(new_position[1])

                                    curr_state.board[new_position[1]] = selected_piece[0]
                            
                            elif piece.color(selected_piece[0]) == piece.black:
                                if new_position[1] // DIMENSION == 3: 
                                    curr_state.en_passant = new_position[1]
                                if new_position[1] // DIMENSION == 7:
                                    curr_state.piece_indices[selected_piece[0]].remove(new_position[1])
                                    
                                    selected_piece = (piece.black | piece.queen, selected_piece[1])

                                    curr_state.piece_indices[selected_piece[0]].append(new_position[1])

                                    curr_state.board[new_position[1]] = selected_piece[0]
                        
                        curr_state.en_passant = None

                        
                        
                        if piece.rank(selected_piece[0]) == piece.king:
                            
                            if piece.color(selected_piece[0]) == piece.white:
                                if curr_state.white_kingside_castling and new_position[1] == 62:
                                    
                                    curr_state.move_piece((piece.white | piece.rook, 63), (-1, 61))

                                    curr_state.white_kingside_castling = 0

                                elif curr_state.white_queenside_castling and new_position[1] == 58:

                                    curr_state.move_piece((piece.white | piece.rook, 56), (-1, 59))

                                    curr_state.white_queenside_castling = 0
                                    
                                curr_state.white_kingmoved = 1
                            elif piece.color(selected_piece[0]) == piece.black:
                                if curr_state.black_kingside_castling and new_position[1] == 6:

                                    curr_state.move_piece((piece.black | piece.rook, 7), (-1, 5))

                                    curr_state.black_kingside_castling = 0

                                elif curr_state.black_queenside_castling and new_position[1] == 2:

                                    curr_state.move_piece((piece.black | piece.rook, 0), (-1, 3))

                                    curr_state.black_queenside_castling = 0


                                curr_state.black_kingmoved = 1

                        if piece.rank(selected_piece[0]) == piece.rook:
                            if piece.color(selected_piece[0]) == piece.white:
                                if selected_piece[1] % 8:
                                    curr_state.white_queensiderook = 1
                                elif (selected_piece[1] + 1) % 8:
                                    curr_state.white_kingsiderook = 1
                            
                            if piece.color(selected_piece[0]) == piece.black:
                                if selected_piece[1] % 8:
                                    curr_state.black_queensiderook = 1
                                elif (selected_piece[1] + 1) % 8:
                                    curr_state.black_kingsiderook = 1
                        
                            print(curr_state.en_passant)
                        

                        
                        
                        curr_state.set_possible_moves()
                        curr_state.checkmate()

                        if curr_state.white_checkmate:
                            running = False
                            print("white_checkmate")
                        if curr_state.black_checkmate:
                            running = False
                            print("black_checkmate")

                        
                        curr_state.switch_turn()

                        
                        selected_piece = None
                        moves = None

                    elif new_position[1] == selected_piece[1]:
                        curr_state.board[selected_piece[1]] = -1
                        curr_state.board[new_position[1]] = selected_piece[0]
                        selected_piece = None
                        moves = None


        drawBoard(screen)
        highlightPossibleMoves(screen, moves)
        drawHighlightedSquare(screen, new_position[1])
        drawPieces(screen, curr_state.board)
        drawSelectedPiece(screen, selected_piece)


        clock.tick(MAX_FPS)
        p.display.flip()







def highlightPossibleMoves(screen, moves):

    if moves:
        for move in moves[1]:
            s = p.Surface((SQ_SIZE,SQ_SIZE))  # the size of your rect
            s.set_alpha(128)                # alpha level
            s.fill(p.Color(BOARD_POSSIBLE_MOVE))           # this fills the entire surface

            if type(move) is int:
                screen.blit(s, (move % DIMENSION * SQ_SIZE,(move // DIMENSION) * SQ_SIZE))
            else:
                for sliding_move in move:
                    screen.blit(s, (sliding_move % DIMENSION * SQ_SIZE,(sliding_move // DIMENSION) * SQ_SIZE))







def drawHighlightedSquare(screen, pos):
    
    s = p.Surface((SQ_SIZE,SQ_SIZE))  # the size of your rect
    s.set_alpha(128)                # alpha level
    s.fill(p.Color(BOARD_HIGHLIGHT))           # this fills the entire surface
    screen.blit(s, (pos%DIMENSION * SQ_SIZE,(pos // DIMENSION) * SQ_SIZE))
    #rect = p.Rect(pos%DIMENSION * SQ_SIZE, (pos // DIMENSION) * SQ_SIZE, SQ_SIZE, SQ_SIZE)
    #p.draw.rect(screen, p.Color(BOARD_HIGHLIGHT), rect)



def drawSelectedPiece(screen, selected_piece):

    if selected_piece:
        image = pieces_image_reference[selected_piece[0]]
        pos = p.Vector2(p.mouse.get_pos())
        screen.blit(IMAGES[image], p.Rect(pos.x - SQ_SIZE // 2, pos.y - SQ_SIZE // 2, SQ_SIZE, SQ_SIZE))


def drawGameState(screen, curr_state):
    drawBoard(screen)

    drawPieces(screen, curr_state)

def drawBoard(screen):

    
    colors = [p.Color(BOARD_LIGHT), p.Color(BOARD_DARK)]

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, curr_state):

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if curr_state[r*DIMENSION + c] >= 0:
                image = pieces_image_reference[curr_state[r*DIMENSION + c]]
                screen.blit(IMAGES[image], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                
    


main()




