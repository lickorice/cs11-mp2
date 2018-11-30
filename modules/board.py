import random

class Board():
    
    def __init__(self, rows, cols, cards=[]):
        """
        This instantiates the Board() class.

        Args:
            rows (int): Number of cards per row
            cols (int): Number of rows
            cards (list): List of Card() objects
        """
        self.rows = rows
        self.cols = cols
        self.cards = cards
    
    def shuffle(self):
        """This function shuffles the cards in place"""
        random.shuffle(self.cards)