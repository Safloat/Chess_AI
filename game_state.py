import numpy
import board
from collections import defaultdict



class piece:

    king = 0b00000    #0
    queen = 0b00001   #1
    bishop = 0b00010  #2
    rook = 0b00011    #3
    knight = 0b00100  #4
    pawn = 0b00101    #5

    white = 0b01000  
    black = 0b10000

    color_mask = white | black

    rank_mask = 0b00111


    def color(_piece):
        return _piece & piece.color_mask
    
    def is_enemy(p1, p2):
        return piece.color(p1) != piece.color(p2)

    def rank(_piece):
        return _piece & piece.rank_mask
        


class game_state:
    
    current_piece_indices=defaultdict(list)
    curr_board = numpy.array([-1]*64)
    print(curr_board)
    #white_castling_info
    white_kingmoved=0
    white_kingsiderook=0
    white_queensiderook=0
    #black_castling_info
    black_kingmoved=0
    black_kingsiderook=0
    black_queensiderook=0
    white_checkmate=0
    black_checkmate=0
    
    en_passant = None

    def init_classic_board():

        game_state.current_piece_indices[piece.black | piece.queen].append(3)
        game_state.current_piece_indices[piece.black | piece.king].append(4)
        game_state.current_piece_indices[piece.black | piece.bishop].extend([2,5])
        game_state.current_piece_indices[piece.black | piece.knight].extend([1,6])
        game_state.current_piece_indices[piece.black | piece.rook].extend([7,0]) 
        for i in range(8):
            game_state.current_piece_indices[piece.black | piece.pawn].append(8 + i) 
       
        game_state.current_piece_indices[piece.white | piece.king].append(60)
        game_state.current_piece_indices[piece.white | piece.queen].append(59)
        game_state.current_piece_indices[piece.white | piece.bishop].extend([58,61])
        game_state.current_piece_indices[piece.white | piece.knight].extend([57,62])
        game_state.current_piece_indices[piece.white | piece.rook].extend([63,56])

        for i in range(8):
            game_state.current_piece_indices[piece.white | piece.pawn].append(48 + i) 
       
        for i in range(32):
            game_state.curr_board[game_state.current_piece_indices[i]] = i
        
        print(game_state.curr_board)

    def pawnmoves(pos, color):

        val_mov=[]
        if pos > 7 and pos < 56:
            if color == piece.black:

                if pos // 8 == 1:
                    if game_state.curr_board[pos + 16] < 0:
                        val_mov.append(pos+16)
                        #en passant check  
                if game_state.curr_board[pos + 8] < 0:
                    if pos < 56:
                        val_mov.append(pos+8)
                if game_state.curr_board[pos + 7] >= 0 and piece.is_enemy(game_state.curr_board[pos + 7], color): 
                    if pos%8 != 0:
                        val_mov.append(pos+7)
                if game_state.curr_board[pos + 9] >= 0 and piece.is_enemy(game_state.curr_board[pos + 9], color):
                    if (pos + 1)%8 == 0:
                        val_mov.append(pos+9)
                
                if pos // 8 == 4:
                    if pos % 8:
                        if game_state.en_passant and pos - 1 == game_state.en_passant:
                            val_mov.append(pos - 1)
                    if (pos + 1) % 8: 
                        if game_state.en_passant and pos + 1 == game_state.en_passant:
                            val_mov.append(pos + 1)
                    
            if color == piece.white:
                if pos // 8 == 6:
                    if game_state.curr_board[pos - 16] < 0:    
                            val_mov.append(pos-16)
                            #en passant check
                if game_state.curr_board[pos - 8] < 0:
                    if pos>7:
                        val_mov.append(pos-8)
                if game_state.curr_board[pos - 9] >= 0 and piece.is_enemy(game_state.curr_board[pos - 9], color): 
                    if pos%8!=0 and pos>=0 and pos<64:
                        val_mov.append(pos-9)
                if game_state.curr_board[pos - 7] >= 0 and piece.is_enemy(game_state.curr_board[pos - 7], color):
                    if (pos + 1)%8 != 0 :
                        val_mov.append(pos-7)


                if pos // 8 == 3:
                    if pos % 8:
                        if game_state.en_passant and pos - 1 == game_state.en_passant:
                            val_mov.append(pos - 1)
                    if (pos + 1) % 8: 
                        if game_state.en_passant and pos + 1 == game_state.en_passant:
                            val_mov.append(pos + 1)


        game_state.verification_of_moves(color, val_mov)
        return val_mov

    def bishopmoves(pos, color):
        val_moves=[]
        cpos=pos
        #loop for upperleft
        while 1:
            if cpos % 8:
                cpos = cpos - 9     
                if cpos >= 0:
                    other_piece = game_state.curr_board[cpos] 
                    if other_piece >= 0:
                        if not piece.is_enemy(other_piece, color):
                            break
                        else:
                            val_moves.append(cpos)
                            break
                    else:
                        val_moves.append(cpos)
                    if cpos % 8 == 0:
                        break
            else:
                break
        cpos=pos
        #loop for upper right
        while 1:
            if (cpos + 1) % 8:
                cpos=cpos-7
                if cpos >= 0:
                    other_piece = game_state.curr_board[cpos] 
                    if other_piece >= 0:
                        if not piece.is_enemy(other_piece, color):
                            break
                        else:
                            val_moves.append(cpos)
                            break
                    else:
                        val_moves.append(cpos)
                    if (cpos+1) % 8 == 0:
                        break
            else:
                break
            
        cpos=pos
        #loop for lower right
        while 1:
            if (cpos + 1) % 8:
                cpos=cpos+9
                if cpos<64:
                    other_piece = game_state.curr_board[cpos] 
                    if other_piece >= 0:
                        if not piece.is_enemy(other_piece, color):
                            break
                        else:
                            val_moves.append(cpos)
                            break
                    else:
                        val_moves.append(cpos)
                    if (cpos + 1) % 8 == 0:
                        break
            else:
                break
        cpos=pos
        #loop for lower left
        while 1:
            if cpos % 8:
                cpos=cpos+7
                if cpos<64:
                    other_piece = game_state.curr_board[cpos] 
                    if other_piece >= 0:
                        if not piece.is_enemy(other_piece, color):
                            break
                        else:
                            val_moves.append(cpos)
                            break
                    else:
                        val_moves.append(cpos)
                    if cpos % 8 == 0:
                        break
            else:
                break
        return val_moves

    def kingmoves(pos, color):
        val_moves=[]
        #top row
        if pos>7 and pos<64:
            val_moves.append(pos-8)
            if pos%8!=0:
                val_moves.append(pos-9)
            if (pos-7)%8!=0:
                val_moves.append(pos-7)
        #left middle value
        if pos%8!=0:
            val_moves.append(pos-1)
        #right middle value
        if (pos + 1)%8!=0:
            val_moves.append(pos+1)

        #bottom row
        if pos>0 and pos<56:
            val_moves.append(pos+8)
            if pos%8!=0:
                val_moves.append(pos+7)
            if (pos + 1)%8!=0:
                val_moves.append(pos+9)

        return game_state.verification_of_moves(color, val_moves)

    def rookmoves(pos, color):
        val_moves=[]
        cpos=pos
        #upwards
        if cpos>7 and cpos<64:
            while 1:
                cpos=cpos-8
                if cpos>=0:
                    other_piece = game_state.curr_board[cpos] 
                    if other_piece >= 0:
                        if not piece.is_enemy(other_piece, color):
                            break
                        else:
                            val_moves.append(cpos)
                            break
                    else:
                        val_moves.append(cpos)
                else:
                    break
        #downwards
        cpos=pos
        if cpos<56 and cpos>0:
            while 1:
                cpos=cpos+8
                if cpos<=63:
                    other_piece = game_state.curr_board[cpos] 
                    if other_piece >= 0:
                        if not piece.is_enemy(other_piece, color):
                            break
                        else:
                            val_moves.append(cpos)
                            break
                    else:
                        val_moves.append(cpos)
                else:
                    break
        #left
        cpos=pos
        if cpos%8!=0 and cpos>=0 and cpos<64:
            while 1:
                cpos=cpos-1
                other_piece = game_state.curr_board[cpos] 
                if other_piece >= 0:
                    if not piece.is_enemy(other_piece, color):
                        break
                    else:
                        val_moves.append(cpos)
                        break
                else:
                    val_moves.append(cpos)
                
                if cpos % 8 == 0:
                    break
                
        
        #right
        cpos=pos
        if (cpos-7)%8!=0 and cpos>=0 and cpos<64:
            while 1:
                cpos=cpos+1
                other_piece = game_state.curr_board[cpos] 
                if other_piece >= 0:
                    if not piece.is_enemy(other_piece, color):
                        break
                    else:
                        val_moves.append(cpos)
                        break
                else:
                    val_moves.append(cpos)
                
                if (cpos-7)%8==0:
                    break
               
        return val_moves

    def queenmoves(pos, color):
        val_moves=[]
        if pos>=0 and pos<64:
            val_moves += game_state.rookmoves(pos, color)
            val_moves += game_state.bishopmoves(pos, color)
        return val_moves

    def knightmoves(pos, color):
        
        val_moves = []

        #can move left
        if pos % 8 > 1:
            
            if pos > 7: #can move up
                val_moves.append(pos - 10)
            if pos < 56:    #can move down
                val_moves.append(pos + 6)
            
        #can move right
        if pos% 8 < 6:
            
            if pos > 7: #can move up
                val_moves.append(pos - 6)
            if pos < 56:    #can move down
                val_moves.append(pos + 10)
        
        #can move up
        if pos > 15:
            if pos % 8: #can move left
                val_moves.append(pos - 17)
            if (pos + 1) % 8:    #can move right
                val_moves.append(pos - 15)

        #can move down
        if pos < 48:
            if pos % 8: #can move left
                val_moves.append(pos + 15)
            if (pos + 1) % 8:    #can move right
                val_moves.append(pos + 17)

        return game_state.verification_of_moves(color, val_moves)

    def check_castling(pos, color):
        res=[]
        if color == piece.white:
            #for kingside
             if game_state.white_kingmoved==0 and game_state.white_kingsiderook==0 and game_state.curr_board[62]<0 and game_state.curr_board[61]<0:
                 res.append("kingside")
             if game_state.white_kingmoved==0 and game_state.white_queensiderook==0 and game_state.curr_board[59]<0 and game_state.curr_board[58]<0 and game_state.curr_board[57]<0:
                 res.append("queenside")
        
        if color == piece.black:
            #for kingside
             if game_state.black_kingmoved==0 and game_state.black_kingsiderook==0 and game_state.curr_board[5]<0 and game_state.curr_board[6]<0:
                 res.append("kingside")
             if game_state.black_kingmoved==0 and game_state.black_queensiderook==0 and game_state.curr_board[1]<0 and game_state.curr_board[2]<0 and game_state.curr_board[3]<0:
                 res.append("queenside")

        return res
    def verification_of_moves(color, moves):
        
        valid_moves = []
        
        for move in moves:
            if not (game_state.curr_board[move] >= 0 and not piece.is_enemy(game_state.curr_board[move],color)):
                valid_moves.append(move)
        
        return valid_moves
                