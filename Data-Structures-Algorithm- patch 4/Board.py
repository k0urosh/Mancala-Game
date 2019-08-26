import numpy as np

class Board:
    
    def __init__ (self, col, seed):
        self.__board = np.zeros(col*2, dtype=np.int32)
        self.__board.fill(seed)
        
    @property
    def board (self):
        return self.__board
    
    @board.setter
    def board (self, b):
        self.__board = b