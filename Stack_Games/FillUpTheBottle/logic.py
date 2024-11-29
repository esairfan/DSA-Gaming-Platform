import random

class FillUpTheBottle:
    def __init__(self, colors):
        self.colors = colors
        self.bottles = self._initialize_game()
        self.moves = 0

    def _initialize_game(self): 
        total_bottles = self.colors + 2
        bottles = [[] for _ in range(total_bottles)]
        balls = [color for color in range(1, self.colors + 1) for _ in range(4)]
        random.shuffle(balls)
 
        for ball in balls:
            while True:
                bottle_idx = random.choice(range(total_bottles))
                if len(bottles[bottle_idx]) < 4:
                    bottles[bottle_idx].append(ball)
                    break

        return bottles

    def is_valid_move(self, source, target):
 
        if not self.bottles[source]: 
            return False
        if not self.bottles[target]: 
            return True 
        return self.bottles[source][-1] == self.bottles[target][-1] and len(self.bottles[target]) < 4
        

    def is_game_complete(self): 
        
        for bottle in self.bottles:
            if bottle and (len(set(bottle)) != 1 or len(bottle) != 4):
                return False
        return True

    def make_move(self, source, target):
 
        if self.is_valid_move(source, target):
            ball = self.bottles[source].pop()
            self.bottles[target].append(ball)
            self.moves += 1 
