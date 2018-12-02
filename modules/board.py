import random

class Board():    
    """
    This class is used in the interface to determine card positioning in terms of a fixed number
    of columns and rows of cards; and also stores the :class:`.Card` objects within the board.

    Attributes:
        rows (int): The number of cards per row.
        cols (int): The number of cards per column.
        cards (list): The `list` of :class:`.Card` objects in the board. Must match `rows * cols`.
    """
    def __init__(self, rows, cols, cards=[]):
        self.rows = rows
        self.cols = cols
        self.cards = cards
    
    def shuffle(self):
        """This function shuffles the cards in place"""
        random.shuffle(self.cards)