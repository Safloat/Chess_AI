import numpy
import board




class piece:

    black_king = 0
    black_queen = 1
    black_bishop = [2, 3]
    black_rook = [4, 5]
    black_knight = [6, 7]
    black_pawn = [i for i in range(8, 16)]

    white_king = 16
    white_queen = 17
    white_bishop = [18, 19]
    white_rook = [20, 21]
    white_knight = [22, 23]
    white_pawn = [i for i in range(24, 32)]



class game_state:
    
    current_piece_indices=numpy.array([-1]*32)
    curr_board = numpy.array([-1]*64)
    print(curr_board)
    #print(curr_board)
    #1 king, 1 queen, 2 bishops, 2 rooks, 2 knights, 8 pawns 
    # Black index0=king, index1=queen, index2=bishop1, index3=bishop2, index4=rook1, index5=rook2, index6=knight1, index7=knight2, index8=pawn1, index9=pawn2, index10=pawn3, index11=pawn4, index12=pawn5, index13=pawn6, index14=pawn7, index15=pawn8
    # White index16=king, index17=queen, index18=bishop1, index19=bishop2, index20=rook1, index21=rook2, index22=knight1, index23=knight2, index24=pawn1, index25=pawn2, index26=pawn3, index27=pawn4, index28=pawn5, index29=pawn6, index30=pawn=7, index31=pawn8


    def init_classic_board():

        game_state.current_piece_indices[piece.black_queen] = 3
        game_state.current_piece_indices[piece.black_king] = 4
        game_state.current_piece_indices[piece.black_bishop[0]] =2
        game_state.current_piece_indices[piece.black_bishop[1]] =5
        game_state.current_piece_indices[piece.black_knight[0]] =1
        game_state.current_piece_indices[piece.black_knight[1]] =6
        game_state.current_piece_indices[piece.black_rook[0]] = 7 
        game_state.current_piece_indices[piece.black_rook[1]] = 0
        for i in range(8):
            game_state.current_piece_indices[piece.black_pawn[i]] = 8 + i 
       
        game_state.current_piece_indices[piece.white_king] = 60
        game_state.current_piece_indices[piece.white_queen] = 59
        game_state.current_piece_indices[piece.white_bishop[0]] =58
        game_state.current_piece_indices[piece.white_bishop[1]] =61
        game_state.current_piece_indices[piece.white_knight[0]] = 57
        game_state.current_piece_indices[piece.white_knight[1]] =62
        game_state.current_piece_indices[piece.white_rook[0]] = 63
        game_state.current_piece_indices[piece.white_rook[1]] = 56
        for i in range(8):
            game_state.current_piece_indices[piece.white_pawn[i]] = 48 + i 
       
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
            cpos=cpos-9
            if cpos>=0 and cpos%8 != 0:
                val_moves.append()
            else:
                break
        cpos=pos
        #loop for upper right
        while 1:
            cpos=cpos-7
            if cpos>=0:
                val_moves.append()
            else:
                break
        
        cpos=pos
        #loop for lower right
        while 1:
            cpos=cpos+9
            if cpos<64:
                val_moves.append()
            else:
                break
        cpos=pos
        #loop for lower left
        while 1:
            cpos=cpos+7
            if cpos<64:
                val_moves.append()
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
            val_moves.append(self.rookmoves(pos))
            val_moves.append(self.bishopmoves(pos))
        return val_moves


        







        


                
    

