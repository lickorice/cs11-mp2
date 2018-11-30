import json, math, random, pyglet
from modules import interface
from modules import board as b
from modules import card as c

class Engine():

    def __init__(self):
        """
        This instantiates the Engine() class.
        """
        self.board = b.Board(0, 0) # always start with an empty set of cards

    def generate_cards(self, pairs):
        """
        This function generates a set of cards to be used in a game.
        """
        rows, cols = 0, 0
        card_number = pairs*2
        square = int(math.sqrt(card_number))
        # Determine the size of the playing field:
        if math.sqrt(card_number) == square:
            # cards are a perfect square
            rows, cols = square, square
        else:
            # try to achieve as close as possible to a square:
            while card_number % square != 0:
                square -= 1 # will always terminate, number is % 2 = 0.
            rows = card_number // square
            cols = square
        self.board.rows = rows
        self.board.cols = cols
        
        with open("assets/cards/config.json") as f:
            all_cards = json.load(f)

        all_cards_keys = list(all_cards.keys())
        random.shuffle(all_cards_keys)
        for i in range(0, 2*pairs, 2):
            card_1 = c.Card(i+1, int(all_cards_keys[(i//2)%len(all_cards_keys)]))
            card_2 = c.Card(i+2, int(all_cards_keys[(i//2)%len(all_cards_keys)]))
            self.board.cards.append(card_1)
            self.board.cards.append(card_2)
        self.board.shuffle()

    def end_game(self):
        self.board = b.Board(0, 0) # empty the board
