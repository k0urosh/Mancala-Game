class Player():
    
    def __init__(self, n):
        self.__name = n
        self.__score = 0
        
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, n):
        self.__name = n
        
    @property
    def score(self):
        return self.__score
    
    @score.setter
    def score(self, s):
        self.__score = s
        
