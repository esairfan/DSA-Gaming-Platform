import random

class TowerOfHanoi:
    def __init__(self, tiles):
        self.tiles = tiles
        self.towers = self._initialize_game()
        self.moves = 0
        self.ranks = [i for i in range(1, tiles + 1)]

    def _initialize_game(self):  
        towers = [[] for _ in range(3)]  
        towers[0] = [i for i in range(self.tiles, 0, -1)]
        return towers

    def is_valid_move(self, source, target):
        if not self.towers[source]: 
            return False
        if not self.towers[target]: 
            return True 
        return self.towers[source][-1] < self.towers[target][-1]
    def is_game_complete(self): 
        return (self.towers[1] == list(range(self.tiles, 0, -1)) or 
                self.towers[2] == list(range(self.tiles, 0, -1)))
     
    def make_move(self, source, target):
        if self.is_valid_move(source, target):
            tile = self.towers[source].pop()
            self.towers[target].append(tile)
            self.moves += 1 
