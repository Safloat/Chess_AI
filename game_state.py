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

    def color(_piece):
        if _piece >> 3 == piece.white >> 3:
            return piece.white
        else:
            return piece.black
    
    def is_enemy(p1, p2):
        return piece.color(p1) != piece.color(p2)
        


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
    #print(curr_board)
    #1 king, 1 queen, 2 bishops, 2 rooks, 2 knights, 8 pawns 
    # Black index0=king, index1=queen, index2=bishop1, index3=bishop2, index4=rook1, index5=rook2, index6=knight1, index7=knight2, index8=pawn1, index9=pawn2, index10=pawn3, index11=pawn4, index12=pawn5, index13=pawn6, index14=pawn7, index15=pawn8
    # White index16=king, index17=queen, index18=bishop1, index19=bishop2, index20=rook1, index21=rook2, index22=knight1, index23=knight2, index24=pawn1, index25=pawn2, index26=pawn3, index27=pawn4, index28=pawn5, index29=pawn6, index30=pawn=7, index31=pawn8


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

    def pawnmoves(self,pos,col):

        val_mov=[]
        if pos > 7 and pos < 56:
            if col=='black':
                temp=8
                for i in range(8):
                    if pos==(temp+i):
                        val_mov.append(pos+16)
                        #en passant check  
                if pos<56:
                    val_mov.append(pos+8)
                if pos%8!=0:
                    val_mov.append(pos+7)
                if (pos-7)%8==0:
                    val_mov.append(pos+9)
                
            if col=='white':
                temp=48
                for i in range(8):
                    if pos==(temp+i):
                        val_mov.append(pos-16)
                        #en passant check
                if pos>7:
                    val_mov.append(pos-8)
                if pos%8!=0 and pos>=0 and pos<64:
                    val_mov.append(pos-9)
                if pos%7!=0 :
                    val_mov.append(pos-7)
        return val_mov

    def bishopmoves(self,pos):
        val_moves=[]
        cpos=pos
        #loop for upperleft
        while 1:
            cpos = cpos - 9
            if cpos >= 0:
                val_moves.append(cpos)
                if cpos % 8 == 0:
                    break
                
            else:
                break
        cpos=pos
        #loop for upper right
        while 1:
            cpos=cpos-7
            if cpos >= 0:
                val_moves.append(cpos)
                if (cpos+1) % 8 == 0:
                    break
            else:
                break
        
        cpos=pos
        #loop for lower right
        while 1:
            cpos=cpos+9
            if cpos<64:
                val_moves.append(cpos)
                if (cpos + 1) % 8 == 0:
                    break
            else:
                break
        cpos=pos
        #loop for lower left
        while 1:
            cpos=cpos+7
            if cpos<64:
                val_moves.append()
                if cpos % 8 == 0:
                    break
            else:
                break
        return val_moves

    def kingmoves(self,pos):
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
        if (pos-7)%8!=0:
            val_moves.append(pos+1)

        #bottom row
        if pos>0 and pos<56:
            val_moves.append(pos+8)
            if pos%8!=0:
                val_moves.append(pos+7)
            if (pos-7)%8!=0:
                val_moves.append(pos+9)
        return val_moves

    def rookmoves(self,pos):
        val_moves=[]
        cpos=pos
        #upwards
        if cpos>7 and cpos<64:
            while 1:
                cpos=cpos-8
                if cpos>=0:
                    val_moves.append(cpos)
                else:
                    break
        #downwards
        cpos=pos
        if cpos<56 and cpos>0:
            while 1:
                cpos=cpos+8
                if cpos<=63:
                    val_moves.append(cpos)
                else:
                    break
        #left
        cpos=pos
        if cpos%8!=0 and cpos>=0 and cpos<64:
            while 1:
                cpos=cpos-1
                if cpos%8==0:
                    break
                else:
                    val_moves.append(cpos)
        
        #right
        cpos=pos
        if (cpos-7)%8!=0 and cpos>=0 and cpos<64:
            while 1:
                cpos=cpos+1
                if (cpos-7)%8==0:
                    break
                else:
                    val_moves.append(cpos)
        return val_moves

    def queenmoves(self,pos):
        val_moves=[]
        if pos>=0 and pos<64:
            val_moves += self.rookmoves(pos)
            val_moves += self.bishopmoves(pos)
        return val_moves

    def knightmoves(self, pos):
        
        val_moves = []

        #can move left
        if pos > (int(pos / 8) * 8 + 1):
            
            if pos > 7: #can move up
                val_moves.append(pos - 10)
            if pos < 56:    #can move down
                val_moves.append(pos + 6)
            
        #can move right
        if pos < (int(pos / 8) * 8 + 6):
            
            if pos > 7: #can move up
                val_moves.append(pos - 6)
            if pos < 56:    #can move down
                val_moves.append(pos + 10)
        #can move up
        if pos > 15:
            if pos > int(pos / 8) * 8: #can move left
                val_moves.append(pos - 17)
            if pos < int(pos / 8) * 8 + 7:    #can move right
                val_moves.append(pos - 15)

        #can move down
        if pos < 48:
            if pos > int(pos / 8) * 8: #can move left
                val_moves.append(pos + 15)
            if pos < int(pos / 8) * 8 + 7:    #can move right
                val_moves.append(pos + 17)
        return val_moves

    def check_castling(self,pos,col):
        res=[]
        if col=="white":
            #for kingside
             if self.white_kingmoved==0 and self.white_kingsiderook==0 and self.curr_board[62]<0 and self.curr_board[61]<0:
                 res.append("kingside")
             if self.white_kingmoved==0 and self.white_queensiderook==0 and self.curr_board[59]<0 and self.curr_board[58]<0 and self.curr_board[57]<0:
                 res.append("queenside")
        
        if col=="black":
            #for kingside
             if self.black_kingmoved==0 and self.black_kingsiderook==0 and self.curr_board[5]<0 and self.curr_board[6]<0:
                 res.append("kingside")
             if self.black_kingmoved==0 and self.black_queensiderook==0 and self.curr_board[1]<0 and self.curr_board[2]<0 and self.curr_board[3]<0:
                 res.append("queenside")

        return res


        







        


                
    

