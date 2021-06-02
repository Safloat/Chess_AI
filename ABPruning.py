
from copy import deepcopy
from game_state import game_state
import math
import random
import sys
<<<<<<< HEAD
import game_state as game_state
=======
>>>>>>> b8c968b39937ff5fc8bea70fe5dfd569fc4a732d
from game_state import piece



<<<<<<< HEAD

=======
>>>>>>> b8c968b39937ff5fc8bea70fe5dfd569fc4a732d
def minimaxRoot(depth, curr_state, isMaximizing, turn):
    
    if turn == piece.white:
        possibleMoves = curr_state.white_moves
    else:
        possibleMoves = curr_state.black_moves
    
    bestMove = -9999
    bestMoveFinal = None
    for moves in possibleMoves:
        for move in moves[1]:   #loop over all possible moves for each set of moves 
<<<<<<< HEAD
            possible_state = deepcopy(curr_state)
            possible_state.move_piece((curr_state.board[moves[0]], moves[0]), (curr_state.board[move], move))
            
            value = max(bestMove, minimax(depth - 1, possible_state,-10000,10000, not isMaximizing))

            if(value > bestMove):
                print("Best score: " ,str(bestMove))
                print("Best move: ",str(bestMoveFinal))
                bestMove = value
                bestMoveFinal = move
    
    return bestMoveFinal

def minimax(depth, curr_state, alpha, beta, is_maximizing, turn):
=======
            possible_state = deepcopy(curr_state)   #create a deep copy of the current state
            possible_state.move_piece((curr_state.board[moves[0]], moves[0]), (curr_state.board[move], move))   #make a move on the possible state
            
            value = max(bestMove, minimax(depth - 1, possible_state, -10000, 10000, not isMaximizing, piece.opposite_color(turn)))

            if(value > bestMove):
                print("Best score: ", str(bestMove))
                print("Best move: ", str(bestMoveFinal))
                bestMove = value
                bestMoveFinal = (moves[0], move)
    
    return bestMoveFinal

def minimax(depth, board, alpha, beta, is_maximizing, turn):
>>>>>>> b8c968b39937ff5fc8bea70fe5dfd569fc4a732d
    if(depth == 0):
        return -evaluation(curr_state)
    if turn==piece.white:
		possibleMoves=curr_state.white_moves
	else:
		possibleMoves=curr_state.black_moves
    if(is_maximizing):
        bestMove = -9999
        for moves in possibleMoves:
			for move in moves[1]:
				move = chess.Move.from_uci(str(x))
				board.push(move)
				bestMove = max(bestMove,minimax(depth - 1, board,alpha,beta, not is_maximizing))
				board.pop()
				alpha = max(alpha,bestMove)
				if beta <= alpha:
					return bestMove
        return bestMove
    else:
        bestMove = 9999
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            bestMove = min(bestMove, minimax(depth - 1, board,alpha,beta, not is_maximizing))
            board.pop()
            beta = min(beta,bestMove)
            if(beta <= alpha):
                return bestMove
        return bestMove


<<<<<<< HEAD
def calculateMove(board):
    possible_moves = board.legal_moves
    if(len(possible_moves) == 0):
        print("No more possible moves...Game Over")
        sys.exit()
    bestMove = None
    bestValue = -9999
    n = 0
    for x in possible_moves:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        boardValue = -evaluation(board)
        board.pop()
        if(boardValue > bestValue):
            bestValue = boardValue
            bestMove = move

    return bestMove

def evaluation(curr_state):
    i = 0
    evaluation = 0
    x = True
    try:
        x = bool(board.piece_at(i).color)
    except AttributeError as e:
        x = x
    while i < 63:
        i += 1
        evaluation = evaluation + (getPieceValue(str(board.piece_at(i))) if x else -getPieceValue(str(board.piece_at(i))))
=======
# def calculateMove(board):
#     possible_moves = board.legal_moves
#     if(len(possible_moves) == 0):
#         print("No more possible moves...Game Over")
#         sys.exit()
#     bestMove = None
#     bestValue = -9999
#     n = 0
#     for x in possible_moves:
#         move = chess.Move.from_uci(str(x))
#         board.push(move)
#         boardValue = -evaluation(board)
#         board.pop()
#         if(boardValue > bestValue):
#             bestValue = boardValue
#             bestMove = move

#     return bestMove

def evaluation(curr_state, turn):
    for _piece in curr_state.board:
        evaluation = evaluation + (getPieceValue(_piece) if piece.is_enemy(turn,) else -getPieceValue(str(board.piece_at(i))))
>>>>>>> b8c968b39937ff5fc8bea70fe5dfd569fc4a732d
    return evaluation


def getPieceValue(piece):
    if(piece == None):
        return 0
    value = 0
    if piece == "P" or piece == "p":
        value = 10
    if piece == "N" or piece == "n":
        value = 30
    if piece == "B" or piece == "b":
        value = 30
    if piece == "R" or piece == "r":
        value = 50
    if piece == "Q" or piece == "q":
        value = 90
    if piece == 'K' or piece == 'k':
        value = 900
    #value = value if (board.piece_at(place)).color else -value
    return value

def main():
    board = chess.Board()
    n = 0
    print(board)
    while n < 100:
        if n%2 == 0:
            move = input("Enter move: ")
            move = chess.Move.from_uci(str(move))
            board.push(move)
        else:
            print("Computers Turn:")
            move = minimaxRoot(3,board,True)
            move = chess.Move.from_uci(str(move))
            board.push(move)
        print(board)
        n += 1
<<<<<<< HEAD
=======




>>>>>>> b8c968b39937ff5fc8bea70fe5dfd569fc4a732d
