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
        self.healing = card_json["healing"]
        self.flipping = 2

        # Initial state of the card:
        self.flipped = True
        self.correct = False

    def flip(self):
        """This function flips the card, if it has been guessed correctly."""
        self.flipping = 0 if not self.flipped else 1
        self.flipped = not self.flipped

    def set_correct(self):
        """This function permanently sets the card correct"""
        self.correct = True
        if self.healing:
            # heal
            print("heal")
            pass

