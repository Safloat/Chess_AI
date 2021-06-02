import numpy
from collections import defaultdict
from copy import deepcopy
from itertools import chain




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
    


    def __init__(self, piece_indices=defaultdict(list), board=numpy.array([-1]*64), white_kingmoved=0, white_kingsiderook=0, white_queensiderook=0, black_kingmoved=0, black_kingsiderook=0,
        black_queensiderook=0, black_queenside_under_attack=0, white_queenside_under_attack=0, black_kingside_under_attack=0, white_kingside_under_attack=0, 
        white_checkmate=0, black_checkmate=0, white_queenside_castling=0, white_kingside_castling=0, black_kingside_castling=0, black_queenside_castling=0, 
        black_moves=[], white_moves=[], checkmating_moves= [], en_passant=None, turn=None):
        
        self.piece_indices= deepcopy(piece_indices)
        #self.possible_moves=defaultdict(list)
        self.board = deepcopy(board)
        
        print(self.board)
        
        #white_castling_info
        self.white_kingmoved=white_kingmoved
        self.white_kingsiderook=white_kingsiderook
        self.white_queensiderook=white_queensiderook
        
        #black_castling_info
        self.black_kingmoved=black_kingmoved
        self.black_kingsiderook=black_kingsiderook
        self.black_queensiderook=black_queensiderook

        self.black_queenside_under_attack = black_queenside_under_attack
        self.white_queenside_under_attack = white_queenside_under_attack

        self.black_kingside_under_attack = black_kingside_under_attack
        self.white_kingside_under_attack = white_kingside_under_attack

        self.white_checkmate=white_checkmate
        self.black_checkmate=black_checkmate

        self.checkmating_moves = checkmating_moves


        self.white_queenside_castling = white_queenside_castling
        self.white_kingside_castling = white_kingside_castling

        self.black_queenside_castling = black_queenside_castling
        self.black_kingside_castling = black_kingside_castling


        self.black_moves = deepcopy(black_moves)
        self.white_moves = deepcopy(white_moves)
        
        self.en_passant = en_passant
        self.turn = turn


    
    def init_classic_board(self):

        self.piece_indices[piece.black | piece.queen].append(3)
        self.piece_indices[piece.black | piece.king].append(4)
        self.piece_indices[piece.black | piece.bishop].extend([2,5])
        self.piece_indices[piece.black | piece.knight].extend([1,6])
        self.piece_indices[piece.black | piece.rook].extend([7,0]) 
        for i in range(8):
            self.piece_indices[piece.black | piece.pawn].append(8 + i) 
       
        self.piece_indices[piece.white | piece.king].append(60)
        self.piece_indices[piece.white | piece.queen].append(59)
        self.piece_indices[piece.white | piece.bishop].extend([58,61])
        self.piece_indices[piece.white | piece.knight].extend([57,62])
        self.piece_indices[piece.white | piece.rook].extend([63,56])

        for i in range(8):
            self.piece_indices[piece.white | piece.pawn].append(48 + i) 
       
        for i in range(32):
            self.board[self.piece_indices[i]] = i
        
        print(self.board)

    def switch_turn(self):
        self.turn = piece.opposite_color(self.turn)

#-------------------------------------------------------- MOVE CALCULATION
    def pawnmoves(self, pos, color):

        val_mov=[]
        if pos > 7 and pos < 56:
            if color == piece.black:

                
                
                if pos < 56:    #forward move
                    if self.board[pos + 8] < 0:
                        val_mov.append(pos+8)
                        if pos // 8 == 1:
                            if self.board[pos + 16] < 0:
                                val_mov.append(pos+16)
                    
                    if pos % 8: #left move
                        if self.board[pos + 7] >= 0 and piece.is_enemy(self.board[pos + 7], color): 
                            
                                val_mov.append(pos+7)
                    if (pos + 1)%8: #right move      
                        if self.board[pos + 9] >= 0 and piece.is_enemy(self.board[pos + 9], color):
                            
                                val_mov.append(pos+9)
                


                if pos // 8 == 4:   #en_passant check on specific row
                    if pos % 8:
                        if self.en_passant and pos - 1 == self.en_passant:
                            val_mov.append(pos - 1)
                    if (pos + 1) % 8: 
                        if self.en_passant and pos + 1 == self.en_passant:
                            val_mov.append(pos + 1)
                    
            
            #same things mirrored for white
            if color == piece.white:
                
                if pos > 7:
                    if pos % 8:
                        if self.board[pos - 9] >= 0 and piece.is_enemy(self.board[pos - 9], color): 
                                val_mov.append(pos-9)
                    if (pos + 1) % 8:
                        if self.board[pos - 7] >= 0 and piece.is_enemy(self.board[pos - 7], color):
                            val_mov.append(pos-7)
                    if self.board[pos - 8] < 0:  
                        val_mov.append(pos-8)
                        if pos // 8 == 6:
                            if self.board[pos - 16] < 0:    
                                    val_mov.append(pos-16)


                if pos // 8 == 3:
                    if pos % 8:
                        if self.en_passant and pos - 1 == self.en_passant:
                            val_mov.append(pos - 1)
                    if (pos + 1) % 8: 
                        if self.en_passant and pos + 1 == self.en_passant:
                            val_mov.append(pos + 1)


        self.verification_of_moves(color, val_mov)
        return val_mov

    def bishopmoves(self, pos, color):
        
        sliding_moves = []
        
        val_moves=[]
        cpos=pos
        #loop for upperleft
        while 1:
            if cpos % 8:
                cpos = cpos - 9     
                if cpos >= 0:
                    other_piece = self.board[cpos] 
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
                    other_piece = self.board[cpos] 
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
                    other_piece = self.board[cpos] 
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
                    other_piece = self.board[cpos] 
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

    def kingmoves(self, pos, color, fill_checkmating_moves = False):
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


        if color == piece.white:
            if not self.white_kingmoved:
                if not self.white_kingsiderook and not self.white_kingside_under_attack:
                    self.white_kingside_castling = 1
                if not self.white_queenside_under_attack and not self.white_queensiderook:
                    self.white_queenside_castling = 1
        
        if color == piece.black:
            if not self.black_kingmoved:
                if not self.black_kingsiderook and not self.black_kingside_under_attack:
                    self.black_kingside_castling = 1
                if not self.black_queensiderook and not self.black_queenside_under_attack:
                    self.black_queenside_castling = 1

        self.add_castling_moves(color, val_moves)

        

        val_moves = self.verification_of_moves(color, val_moves)
        
        return [move for move in val_moves if not self.check_under_attack(color, move, fill_checkmating_moves)]
        

    def rookmoves(self, pos, color):
        
        sliding_moves = []
        val_moves=[]
        cpos=pos
        #upwards
        if cpos>7 and cpos<64:
            while 1:
                cpos=cpos-8
                if cpos>=0:
                    other_piece = self.board[cpos] 
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
                    other_piece = self.board[cpos] 
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
                other_piece = self.board[cpos] 
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
                other_piece = self.board[cpos] 
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

    def queenmoves(self, pos, color):
        val_moves=[]
        if pos>=0 and pos<64:
            val_moves += self.rookmoves(pos, color)
            val_moves += self.bishopmoves(pos, color)
        return val_moves

    def knightmoves(self, pos, color):
        
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

        

        return self.verification_of_moves(color, val_moves)

    
    #move a piece from one position to another
    def move_piece(self, selected_piece, possible_piece):
        self.board[selected_piece[1]] = -1
        self.board[possible_piece[1]] = selected_piece[0]
        self.piece_indices[selected_piece[0]].remove(selected_piece[1])
        self.piece_indices[selected_piece[0]].append(possible_piece[1])
        if possible_piece[0] >= 0:
            self.piece_indices[possible_piece[0]].remove(possible_piece[1])


    
    #verify whether a set of moves is valid
    def verification_of_moves(self, color, moves):
        
        valid_moves = []
        
        for move in moves:
            if not (self.board[move] >= 0 and not piece.is_enemy(self.board[move],color)):
                valid_moves.append(move)
        
        return valid_moves


    #get valid moves for a piece
    def get_valid_moves(self, selected_piece):

        if selected_piece:
            if piece.rank(selected_piece[0]) == piece.king:
                moves = self.kingmoves(selected_piece[1], piece.color(selected_piece[0]))
            elif piece.rank(selected_piece[0]) == piece.queen:
                moves = self.queenmoves(selected_piece[1], piece.color(selected_piece[0]))
            elif piece.rank(selected_piece[0]) == piece.rook:
                moves = self.rookmoves(selected_piece[1], piece.color(selected_piece[0]))
            elif piece.rank(selected_piece[0]) == piece.bishop:
                moves = self.bishopmoves(selected_piece[1], piece.color(selected_piece[0]))
            elif piece.rank(selected_piece[0]) == piece.knight:
                moves = self.knightmoves(selected_piece[1], piece.color(selected_piece[0]))
            elif piece.rank(selected_piece[0]) == piece.pawn:
                moves = self.pawnmoves(selected_piece[1], piece.color(selected_piece[0]))
            
        return selected_piece[1], moves #return moves with starting position

    #get all valid moves for a team
    def get_all_valid_moves(self, turn, check_castling = True):

        all_moves = []
        for _piece, positions in self.piece_indices.items():
            color = piece.color(_piece)
            if color == turn:
                for position in positions:
                    
                    moves = temp_castling_moves = self.get_valid_moves((_piece, position))
                    if piece.rank(_piece) in [piece.rook, piece.queen, piece.bishop]:
                        print(moves)
                        temp_castling_moves = list(chain.from_iterable(temp_castling_moves[1]))
                        for move in moves[1]:
                            all_moves.append((moves[0], move)) 
                    else:
                        temp_castling_moves = temp_castling_moves[1]
                        all_moves.append(moves)

                    if check_castling:
                        self.castling_under_attack(temp_castling_moves, piece.opposite_color(color))
        
        return all_moves

    


    def set_possible_moves(self):
        
        self.white_moves.clear()
        
        for move in self.get_all_valid_moves(piece.white):
            self.white_moves.append(move)

        self.black_moves.clear()

        for move in self.get_all_valid_moves(piece.black):
            self.black_moves.append(move)

#------------------------------------------------------------ CASTLING CALCULATIONS
    def castling_under_attack(self, moves, color):

        
        self.black_kingside_under_attack = 0
        self.black_queenside_under_attack = 0

        self.white_kingside_under_attack = 0
        self.white_queenside_under_attack = 0

        if color == piece.white:
            print("castling white check")
            for move in moves:
                if move in [1, 2, 3]:
                    print("castling black queenside under attack")
                    self.black_queenside_under_attack = 1
                elif move in [5, 6]:
                    print("castling black kingside under attack")
                    self.black_kingside_under_attack = 1
        
        elif color == piece.black:
            print("castling black check")

            for move in moves:
                if move in [57, 58, 59]:
                    print("castling white queenside under attack")
                    self.white_queenside_under_attack = 1
                elif move in [61, 62]:
                    print("castling white kingside under attack")
                    self.white_kingside_under_attack = 1

        print(moves)


    def add_castling_moves(self, color, val_moves):
        
        if color == piece.white:
            if self.white_kingside_castling:
                if self.board[61] + self.board[62] < -1:
                    val_moves.append(62)
                
            if self.white_queenside_castling:
                if self.board[57] + self.board[58] + self.board[59] < -2:
                    val_moves.append(59)  
        
        else:
            if self.black_kingside_castling:
                if self.board[5] + self.board[6] < -1:
                    val_moves.append(6)
                
            if self.black_queenside_castling:
                if self.board[1] + self.board[2] + self.board[3] < -2:
                    val_moves.append(3)  


#---------------------------------------------------------------CHECKMATING
    #checks if the opposite team is checkmating the given color's king
    def evaluate_checkmate(self, color):
        
        if color == piece.white:
            print(self.black_moves)
            for moves in self.black_moves:
                
                for move in moves[1]:
                    if self.board[move] == piece.white | piece.king:
                        self.white_checkmate = 1
                        return self.endgame_check((piece.white | piece.king, move),self.white_moves, self.black_moves)

        else:
            for moves in self.white_moves:
                for move in moves[1]:
                    if self.board[move] == piece.black | piece.king:
                        self.black_checkmate = 1
                        return self.endgame_check((piece.black | piece.king, move), self.black_moves, self.white_moves)
        


        return False


    #reset checkmate variable if the king can escape
    def endgame_check(self, _piece, defender_moves, attacker_moves): 
    
        
        color = piece.color(_piece[0])
        escape_moves = self.kingmoves(_piece[1], color, True)

      
        if escape_moves:

            under_attack = False
            for move in escape_moves:
                if self.board[move] >=0:
                    new_state = deepcopy(self)
                    new_state.move_piece(_piece, (self.board[move], move))
                    
                    new_state.set_possible_moves()
                    under_attack = new_state.check_under_attack(color,move)
            
            if under_attack:
                return


            if color == piece.white:
                self.white_checkmate = 0
            else:
                self.black_checkmate = 0
            return
     
        else:
            if len(self.checkmating_moves) < 2:
                
                for d_move in defender_moves:
                    for c_move in self.checkmating_moves:
                        if len(set(d_move[1]).intersection(set(c_move[1]))) > 1 or c_move[0] in d_move[1]:
                            if  color == piece.white:
                                self.white_checkmate = 0
                            else:
                                self.black_checkmate = 0
                            return 
                
                return
            

    #check if any piece is under attack and fill checkmating moves if needed
    def check_under_attack(self, color, defender_position, fill_checkmating_moves = False):
        
        
        if color == piece.white:
            print(self.black_moves)
            for moves in self.black_moves:
                
                for move in moves[1]:
                    if move == defender_position:
                        if fill_checkmating_moves:
                            self.checkmating_moves.append(moves)
                        return True
        else:
            for moves in self.white_moves:
                for move in moves[1]:
                    if move == defender_position:
                        if fill_checkmating_moves:
                            self.checkmating_moves.append(moves)
                        return True

        return False
        
    

    #checkmate evaluation for both teams
    def checkmate(self):


        self.evaluate_checkmate(piece.white)
        self.evaluate_checkmate(piece.black)

    