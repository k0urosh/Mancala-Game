import numpy as np
import Player
import Board

class Mancala:
    def __init__ (self, col, seed, name1, name2):
        self.__board = Board.Board(col, seed)
        self.__p1 = Player.Player(name1)
        self.__p2 = Player.Player(name2)
        self.__turn = True
        self.__winCond = np.zeros((col), dtype=np.int32)
                                
    def checkGameState(self):
        count = 0
        arr = []
        flag = False
        for x in range (0, len(self.board.board)):
            if self.board.board[x] != 0:
               count = count + 1
               arr.append(self.board.board[x])
               
        if count <= 2:
            if count == 2 and (arr[0] <= 1 or arr[1] <= 1):
                flag = True
            if count < 2:
                flag = True
               
        arr = np.split(self.board.board, 2)
        if flag == True or np.array_equal(arr[0],self.winCond) == True or np.array_equal(arr[1],self.winCond) == True:    
            for x in range(0, int(len(self.board.board)/2)):
                self.p1.score = self.p1.score + self.board.board[x]
            for x in range(int(len(self.board.board)/2), len(self.board.board)):
                self.p2.score = self.p2.score + self.board.board[x]               
            return False       
        return True
    
    @property
    def turn (self):
        return self.__turn
    
    @turn.setter
    def turn (self, t):
        self.__turn = t

    @property
    def winCond (self):
        return self.__winCond
    
    @winCond.setter
    def winCond (self, w):
        self.__winCond = w

    @property
    def board (self):
        return self.__board
    
    @board.setter
    def board (self, b):
        self.__board = b
    
    @property
    def p1 (self):
        return self.__p1
    
    @p1.setter
    def p1 (self, n):
        self.__p1 = n
        
    @property
    def p2 (self):
        return self.__p2
    
    @p2.setter
    def p2 (self, n):
        self.__p2 = n
            