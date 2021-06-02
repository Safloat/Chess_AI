
from copy import deepcopy
from game_state import game_state
import math
import random
import sys
from game_state import piece



def minimaxRoot(depth, curr_state, isMaximizing, turn):
    
    if turn == piece.white:
        possibleMoves = curr_state.white_moves
    else:
        possibleMoves = curr_state.black_moves
    
    bestMove = -9999
    bestMoveFinal = None
    for moves in possibleMoves:
        for move in moves[1]:   #loop over all possible moves for each set of moves 
            possible_state = deepcopy(curr_state)   #create a deep copy of the current state
            possible_state.move_piece((possible_state.board[moves[0]], moves[0]), (possible_state.board[move], move))   #make a move on the possible state
            
            possible_state.set_possible_moves()

            value = max(bestMove, minimax(depth - 1, possible_state, -10000, 10000, not isMaximizing, piece.opposite_color(turn)))

            if(value > bestMove):
                print("Best score: ", str(bestMove))
                print("Best move: ", str(bestMoveFinal))
                bestMove = value
                bestMoveFinal = (moves[0], move)
    
    return bestMoveFinal

def minimax(depth, curr_state, alpha, beta, is_maximizing, turn):
    if(depth == 0):
        return -evaluation(curr_state, turn)
    
    if turn==piece.white:
        possibleMoves=curr_state.white_moves
    else:
        possibleMoves=curr_state.black_moves
    
    if(is_maximizing):
        bestMove = -9999
        for moves in possibleMoves:
            for move in moves[1]:
                possible_state = deepcopy(curr_state)   #create a deep copy of the current state
                possible_state.move_piece((possible_state.board[moves[0]], moves[0]), (possible_state.board[move], move))

                possible_state.set_possible_moves()

                bestMove = max(bestMove,minimax(depth - 1,possible_state,alpha,beta, not is_maximizing, piece.opposite_color(turn)))
                alpha = max(alpha,bestMove)
                if beta <= alpha:
                    return bestMove
        return bestMove
    else:
        bestMove = 9999
        for moves in possibleMoves:
            for move in moves[1]:
                possible_state = deepcopy(curr_state)   #create a deep copy of the current state
                possible_state.move_piece((possible_state.board[moves[0]], moves[0]), (possible_state.board[move], move))

                possible_state.set_possible_moves()
                
                bestMove = min(bestMove, minimax(depth - 1, possible_state,alpha,beta, not is_maximizing, piece.opposite_color(turn)))
        
                beta = min(beta,bestMove)
                if(beta <= alpha):
                    return bestMove
        return bestMove


def evaluation(curr_state, turn):
    for _piece in curr_state.board:
        evaluation = evaluation + getPieceValue(_piece) if not piece.is_enemy(_piece, turn) else -getPieceValue(_piece)
    return evaluation


def getPieceValue(_piece):
    if(_piece == -1):
        return 0
    value = 0
    rank = piece.rank(_piece)
    if rank == piece.pawn:
        value = 10
    if rank == piece.knight:
        value = 30
    if rank == piece.bishop:
        value = 30
    if rank == piece.rook:
        value = 50
    if rank == piece.queen:
        value = 90
    if rank == piece.king:
        value = 900
    #value = value if (board.piece_at(place)).color else -value
    return value