import pygame as p
from game_state import piece
from game_state import game_state
import numpy as np
import pieces
import board
from collections import defaultdict


WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION

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

    game_state.init_classic_board()

    curr_state = game_state.curr_board
    loadImages()
    running = True

    selected_piece = None

    while running:
        
        possible_piece = get_square_under_mouse(game_state.curr_board)

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            if e.type == p.MOUSEBUTTONDOWN:
                if not selected_piece:
                    if possible_piece[0] >= 0:
                        selected_piece = possible_piece
                        game_state.curr_board[selected_piece[1]] = -1
                elif (game_state.curr_board[possible_piece[1]] >= 0 and piece.is_enemy(possible_piece[0], selected_piece[0])) \
                or game_state.curr_board[possible_piece[1]] < 0:
                    game_state.curr_board[selected_piece[1]] = -1
                    game_state.curr_board[possible_piece[1]] = selected_piece[0]
                    selected_piece = None

        
        drawGameState(screen, curr_state)
        drawHighlightedSquare(screen, possible_piece[1])
        drawSelectedPiece(screen, selected_piece)


        clock.tick(MAX_FPS)
        p.display.flip()


def drawHighlightedSquare(screen, pos):
    
    rect = p.Rect(pos%DIMENSION * SQ_SIZE, (pos // DIMENSION) * SQ_SIZE, SQ_SIZE, SQ_SIZE)
    p.draw.rect(screen, p.Color("green"), rect, 5)



def drawSelectedPiece(screen, selected_piece):

    if selected_piece:
        image = pieces_image_reference[selected_piece[0]]
        pos = p.Vector2(p.mouse.get_pos())
        screen.blit(IMAGES[image], p.Rect(pos.x - SQ_SIZE // 2, pos.y - SQ_SIZE // 2, SQ_SIZE, SQ_SIZE))


def drawGameState(screen, curr_state):
    drawBoard(screen)

    drawPieces(screen, curr_state)

def drawBoard(screen):

    colors = [p.Color("gray"), p.Color("black")]

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




