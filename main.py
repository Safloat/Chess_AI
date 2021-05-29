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

pieces_image_reference = {}
    
pieces_image_reference[game_state.piece.white | game_state.piece.pawn] = 'wp'  
pieces_image_reference[game_state.piece.white | game_state.piece.rook] = 'wR'  
pieces_image_reference[game_state.piece.white | game_state.piece.knight] = 'wN' 
pieces_image_reference[game_state.piece.white | game_state.piece.bishop] = 'wB' 
pieces_image_reference[game_state.piece.white | game_state.piece.king] = 'wK' 
pieces_image_reference[game_state.piece.white | game_state.piece.queen] = 'wQ' 

pieces_image_reference[game_state.piece.black | game_state.piece.pawn] = 'bp' 
pieces_image_reference[game_state.piece.black | game_state.piece.rook] = 'bR'  
pieces_image_reference[game_state.piece.black | game_state.piece.knight] = 'bN' 
pieces_image_reference[game_state.piece.black | game_state.piece.bishop] = 'bB'  
pieces_image_reference[game_state.piece.black | game_state.piece.king] = 'bK' 
pieces_image_reference[game_state.piece.black | game_state.piece.queen] = 'bQ' 



def loadImages():

    print("got here")
    

    for piece, sprite in pieces_image_reference.items():
        IMAGES[sprite] = p.transform.scale(p.image.load("images/" + sprite + ".png"), (SQ_SIZE, SQ_SIZE)) 
    

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
                image = pieces_image_reference[curr_state[r*DIMENSION + c]]
                screen.blit(IMAGES[image], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                
    


main()