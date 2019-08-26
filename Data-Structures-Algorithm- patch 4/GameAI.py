import copy
import numpy as np
import math

class AI:
    def __init__ (self, board, player):
        self.board = board
        self.player = player        
        self.score = 0
        self.move = 0
        self.temp = -math.inf
        
    def alphaBeta(self, node, alpha, beta, depth, maximiser):
        children = []     
        moves = []

        arr = np.asarray(node)
        if depth == 0 or (np.all(node[0:int(len(arr)/2)] == 0) == True) or (np.all(node[int(len(arr)/2):len(arr)] == 0) == True) :
            return self.score
         
        moves = self.getAvailableMoves()           
        if maximiser == True:   
            self.player = True
            for m in moves:                                 
                children.append(self.simulate(m, copy.copy(node), maximiser))
                alpha = max(alpha, self.alphaBeta(children[-1], alpha, beta, depth-1, False))                    
                if(alpha >= beta):
                    break                    
                if(depth == 3):
                    if(alpha > self.temp):   
                        self.temp = alpha
                        self.move = m                         
            return alpha
        else:
            self.player = False
            for m in moves: 
                children.append(copy.copy(self.simulate(m, copy.copy(node), maximiser)))
                beta = min(beta, self.alphaBeta(children[-1], alpha, beta, depth-1, True))                    
                if(alpha >= beta):
                    break
            return beta
    
        
    def simulate(self, move, copyBoard, maximiser):
        seed = copyBoard[move]
        copyBoard[move] = 0
        i = move
        
        while seed != 0:
            if(i+1 < len(copyBoard)):
                i = i + 1
            else:
                i = 0
            copyBoard[i] = copyBoard[i] + 1
            seed = seed - 1
            
        if i+1 == len(copyBoard):
            x = 0
        else:
            x = i+1
        if copyBoard[x] != 0:
            self.simulate(x, copyBoard, maximiser)
        else:
            if x+1 == len(copyBoard):
                x = 0
            else:
                x = x + 1
            if(maximiser == True):
                self.score = self.score + copyBoard[x]
            else:
                self.score = self.score - copyBoard[x]
            copyBoard[x] = 0
        return copyBoard

        

    def getAvailableMoves(self):
        moves = []
        if(self.player == True):
            for x in range(0, int(len(self.board)/2)):
                if(self.board[x] != 0):
                    moves.append(x)
        if(self.player == False):
            for x in range(int(len(self.board)/2), len(self.board)):
                if(self.board[x] != 0):
                    moves.append(x)
        return moves