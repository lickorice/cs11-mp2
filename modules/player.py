class Player():
    """
    The class that stores the data for the game, and later on
    to be submitted to the SQLite database.

    Args:
        board_size (int): The player's current board size (number of cards)(deprecated).
        health (int): The number of hearts the player still has
        level (:obj:`int`, optional): The player's maximum level achieved. Defaults to 1. It can be explicitly
            assigned a value for the purpose of passing the object to the scoreboard.
        name (str): The player name.
        score (:obj:`int`, optional): The player's score. Defaults to 0. It can be explicitly
            assigned a value for the purpose of passing the object to the scoreboard.

    Attributes:
        board_size (int): The player's current board size (number of cards)(deprecated).
        health (int): The number of hearts the player still has
        level (:obj:`int`, optional): The player's maximum level achieved.
        name (str): The player name.
        score (:obj:`int`, optional): The player's score.
    """
    def __init__(self, name, board_size, score=0, level=1):
        self.name = name
        self.score = score
        self.board_size = board_size
        self.health = 3
        self.level = level