class Player():
    def __init__(self, name, board_size, score=0, level=1):
        self.name = name
        self.score = score
        self.board_size = board_size
        self.health = 3
        self.level = level