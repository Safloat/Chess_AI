import numpy
import board
from collections import defaultdict


class piece_move_list:

    def __init__(self, position, moves = []):
        self.position = position
        self.moves = moves 

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

    def opposite_color(_piece):
        return (~(_piece >> 3) << 3) & piece.color_mask

    
        
        


class game_state:
    
    current_piece_indices=defaultdict(list)
    possible_moves=defaultdict(list)
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

    black_queenside_under_attack = 0
    white_queenside_under_attack = 0

    black_kingside_under_attack = 0
    white_kingside_under_attack = 0

    white_checkmate=0
    black_checkmate=0

    white_queenside_castling = 0
    white_kingside_castling = 0

    black_queenside_castling = 0
    black_kingside_castling = 0


    black_moves = []
    white_moves = []
    
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
                
                if pos < 56:
                    if game_state.curr_board[pos + 8] < 0:
                            val_mov.append(pos+8)
                    
                    if pos % 8:
                        if game_state.curr_board[pos + 7] >= 0 and piece.is_enemy(game_state.curr_board[pos + 7], color): 
                            
                                val_mov.append(pos+7)
                    if (pos + 1)%8:                   
                        if game_state.curr_board[pos + 9] >= 0 and piece.is_enemy(game_state.curr_board[pos + 9], color):
                            
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
                
                if pos > 7:
                    if pos % 8:
                        if game_state.curr_board[pos - 9] >= 0 and piece.is_enemy(game_state.curr_board[pos - 9], color): 
                                val_mov.append(pos-9)
                    if (pos + 1) % 8:
                        if game_state.curr_board[pos - 7] >= 0 and piece.is_enemy(game_state.curr_board[pos - 7], color):
                            val_mov.append(pos-7)
                    if game_state.curr_board[pos - 8] < 0:  
                        val_mov.append(pos-8)


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
        
        sliding_moves = []
        
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

        if val_moves:
            sliding_moves.append(val_moves)
        
        val_moves = []
        
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

        if val_moves:
            sliding_moves.append(val_moves)
        
        val_moves = []
            
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

        if val_moves:
            sliding_moves.append(val_moves)
        
        val_moves = []


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

        if val_moves:
            sliding_moves.append(val_moves)
        


        return sliding_moves

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
            if pos % 8!=0:
                val_moves.append(pos+7)
            if (pos + 1) % 8!=0:
                val_moves.append(pos+9)

        return game_state.verification_of_moves(color, val_moves)

    def rookmoves(pos, color):
        
        sliding_moves = []
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
        if val_moves:
            sliding_moves.append(val_moves)
        
        val_moves = []
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

        if val_moves:
            sliding_moves.append(val_moves)
        
        val_moves = []
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
                
        if val_moves:
            sliding_moves.append(val_moves)
        
        val_moves = []
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
        if val_moves:
            sliding_moves.append(val_moves)
        
               
        return sliding_moves

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

        if color == piece.white:
            if not game_state.white_kingmoved:
                if not game_state.white_kingsiderook and not game_state.white_kingside_under_attack:
                    game_state.white_kingside_castling = 1
                if not game_state.white_queenside_under_attack and not game_state.white_queensiderook:
                    game_state.white_queenside_castling = 1
        
        if color == piece.black:
            if not game_state.black_kingmoved:
                if not game_state.black_kingsiderook and not game_state.black_kingside_under_attack:
                    game_state.black_kingside_castling = 1
                if not game_state.black_queensiderook and not game_state.black_queenside_under_attack:
                    game_state.black_queenside_castling = 1

        
        game_state.add_castling_moves(color, val_moves)
        return game_state.verification_of_moves(color, val_moves)


    def add_castling_moves(color, val_moves):
        
        if color == piece.white:
            if game_state.white_kingside_castling:
                if game_state.curr_board[61] + game_state.curr_board[62] < -1:
                    val_moves.append(62)
                
            if game_state.white_queenside_castling:
                if game_state.curr_board[57] + game_state.curr_board[58] + game_state.curr_board[59] < -2:
                    val_moves.append(58)
                    val_moves.append(59)  
        
        else:
            if game_state.black_kingside_castling:
                if game_state.curr_board[5] + game_state.curr_board[6] < -1:
                    val_moves.append(6)
                
            if game_state.black_queenside_castling:
                if game_state.curr_board[1] + game_state.curr_board[2] + game_state.curr_board[3] < -2:
                    val_moves.append(2)
                    val_moves.append(3)  

    def verification_of_moves(color, moves):
        
        valid_moves = []
        
        for move in moves:
            if not (game_state.curr_board[move] >= 0 and not piece.is_enemy(game_state.curr_board[move],color)):
                valid_moves.append(move)
        
        return valid_moves
                
    def castling_under_attack(moves, color):

        if color == piece.white:
            for move in moves:
                if move in [1, 2, 3]:
                    game_state.black_queenside_under_attack = 1
                    break
                elif move in [5, 6]:
                    game_state.black_kingside_under_attack = 1
        
        elif color == piece.black:
            for move in moves:
                if move in [57, 58, 59]:
                    game_state.white_queenside_under_attack = 1
                    break
                elif move in [61, 62]:
                    game_state.white_kingside_under_attack = 1


    #checks if a set of moves is checkmating the given color's king
    def evaluate_checkmate(color):
        
        if color == piece.white:
            for move in game_state.black_moves:
                if game_state.curr_board[move] == piece.white | piece.king:
                    game_state.white_checkmate = 1
                    return game_state.endgame_check((piece.white | piece.king, move),game_state.white_moves, game_state.black_moves)

        else:
            for move in game_state.white_moves:
                if game_state.curr_board[move] == piece.black | piece.king:
                    game_state.black_checkmate = 1
                    return game_state.endgame_check((piece.black | piece.king, move), game_state.black_moves, game_state.white_moves)
        


        return False


     
    '''    
    def is_checkmating(color, defender):

        moves = game_state.get_all_valid_moves(color, False)

        return game_state.evaluate_checkmate(piece.opposite_color(color), moves)     
        
    '''
    def endgame_check(_piece, defender_moves, attacker_moves): #where pos is attacker position colr is colour of king
    
        
        color = piece.color(_piece[0])
        king_moves = game_state.get_valid_moves(_piece)

        escape_moves = []
        checkmating_moves = []

        for move in king_moves:

            flag = True
            for moves in attacker_moves:
                if move in moves[1]:
                    flag = False
                    checkmating_moves.append(moves)
                    break
            if flag:
                escape_moves.append(move)

    #check if king can move out of the way, just get lists of valid king movescompare them with enemy colour's valid moves, pop out the moves that put king under attack
      
        if escape_moves:
            if  color == piece.white:
                game_state.white_checkmate = 0
            else:
                game_state.black_checkmate = 0
            return False
        # else:
        #     if defender_moves

       #if list is not empty
            #self.colour_checkmate=0
            #return
        else:
            if len(checkmating_moves) < 2:
                
                for d_move in defender_moves:
                    for a_move in attacker_moves:
                        if len(set(d_move[1]).intersection(set(a_move[1]))) > 1:
                            if  color == piece.white:
                                game_state.white_checkmate = 0
                            else:
                                game_state.black_checkmate = 0
                            return False
                
                return True
            
        #else
            #check if king can attack the piece that can kill it
                #if yes then checkmate=0
                #return
            #if no
                #check all friend pieces if attacker position can be reached by some other friend piece
                    #if yes= move the piece
                        #checkmate=0
                    #if no
                        #return checkmate=1

    def get_all_valid_moves(turn, check_castling = True):

        all_moves = []
        for _piece, positions in game_state.current_piece_indices.items():
            color = piece.color(_piece)
            if color == turn:
                for position in positions:
                    
                    moves = game_state.get_valid_moves((_piece, position))
                    if(piece.rank(_piece) in [piece.rook, piece.queen, piece.bishop]):
                        temp = []
                        for move in moves[1]:
                            all_moves += (moves[0], move) 
                    else:
                        all_moves += moves

                    if check_castling:
                        game_state.castling_under_attack(moves, piece.opposite_color(color))
        
        return all_moves

    def get_valid_moves(selected_piece):

        if selected_piece:
            if piece.rank(selected_piece[0]) == piece.king:
                moves = game_state.kingmoves(selected_piece[1], piece.color(selected_piece[0]))
            elif piece.rank(selected_piece[0]) == piece.queen:
                moves = game_state.queenmoves(selected_piece[1], piece.color(selected_piece[0]))
            elif piece.rank(selected_piece[0]) == piece.rook:
                moves = game_state.rookmoves(selected_piece[1], piece.color(selected_piece[0]))
            elif piece.rank(selected_piece[0]) == piece.bishop:
                moves = game_state.bishopmoves(selected_piece[1], piece.color(selected_piece[0]))
            elif piece.rank(selected_piece[0]) == piece.knight:
                moves = game_state.knightmoves(selected_piece[1], piece.color(selected_piece[0]))
            elif piece.rank(selected_piece[0]) == piece.pawn:
                moves = game_state.pawnmoves(selected_piece[1], piece.color(selected_piece[0]))
            
        return selected_piece[1], moves


    def set_possible_moves():
        
        game_state.white_moves.clear()
        game_state.white_moves.extend(game_state.get_all_valid_moves(piece.white))

        game_state.black_moves.clear()
        game_state.black_moves.extend(game_state.get_all_valid_moves(piece.black))


    def checkmate():


        game_state.evaluate_checkmate(piece.white)
        game_state.evaluate_checkmate(piece.black)

        
'''     
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
'''