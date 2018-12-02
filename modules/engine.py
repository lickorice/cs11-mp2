import json, math, random, pyglet
from modules import interface
from modules import board as b
from modules import card as c
from modules import player as p
from data import db_player

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

        self.board.cards = []

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

    def get_scoreboard(self):
        """Fetches the top 20 players in the database."""
        player_db = db_player.PlayerDB()
        player_db.connect()
        entries = player_db.get_players()
        player_db.close()

        player_list = []
        for entry in entries:
            
            player = p.Player(
                entry["user_name"], 
                0, 
                entry["user_score"],
                entry["user_level"]
                )
            player_list.append(player)

        player_list = sorted(player_list, key=lambda x: x.score)[::-1]
        return player_list[:9]

    def submit_to_scoreboard(self, name, level, score):
        """
        This function submits to the scoreboard's database.

        Args:
            name (str): The player's name
            level (int): The player's level (on getting defeated)
            score (int): The player's score
        """
        player_db = db_player.PlayerDB()
        player_db.connect()
        player_db.add_player(name, level, score)
        player_db.close()