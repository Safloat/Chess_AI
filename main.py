import pygame as p
import game_state
import numpy as np
import pieces
import board
from collections import defaultdict


WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION

MAX_FPS = 30

IMAGES = {}

pieces_image_reference = defaultdict(list)
    
pieces_image_reference['wp'] = game_state.piece.white_pawn 
pieces_image_reference['wR'] = game_state.piece.white_rook
pieces_image_reference['wN'] = game_state.piece.white_knight 
pieces_image_reference['wB'] = game_state.piece.white_bishop 
pieces_image_reference['wK'] = [game_state.piece.white_king]
pieces_image_reference['wQ'] = [game_state.piece.white_queen]
pieces_image_reference['bp'] = game_state.piece.black_pawn
pieces_image_reference['bR'] = game_state.piece.black_rook
pieces_image_reference['bN'] = game_state.piece.black_knight
pieces_image_reference['bB'] = game_state.piece.black_bishop
pieces_image_reference['bK'] = [game_state.piece.black_king]
pieces_image_reference['bQ'] = [game_state.piece.black_queen]



def loadImages():

    print("got here")
    

    for piece, value in pieces_image_reference.items():
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)) 
    

def main():

    p.init()
    print("inited")
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()

    screen.fill(p.Color("white"))

    game_state.game_state.init_classic_board()

    curr_state = game_state.game_state.curr_board
    loadImages()
    running = True

    while running:
        
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState(screen, curr_state)

        clock.tick(MAX_FPS)
        p.display.flip()


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
                for image, values in pieces_image_reference.items():
                    #print(curr_state)
                    if np.isin(curr_state[r*DIMENSION + c],values):
                        screen.blit(IMAGES[image], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                        break
                
    


main()