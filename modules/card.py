import json

with open("assets/cards/config.json") as f:
    config = json.load(f)

class Card():
    def __init__(self, card_id, card_key):
        """
        This initializes the Card class.

        Args:
            card_id (int): The unique identifier for the card,
            card_key (int): The card to be used, according to the .json.
        """
        self.id = card_id

        # Data passed in from the .json:

        card_json = config[str(card_key)]
        self.key = card_key
        self.content = card_json["content"]
        self.img_url = card_json["img_url"]

        # Initial state of the card:
        self.flipped = False
        self.correct = False

    def flip(self):
        """This function flips the card, if it has been guessed correctly."""
        self.flipped = False if self.flipped else True

    def set_correct(self):
        """This function permanently sets the card correct"""
        self.correct = True

