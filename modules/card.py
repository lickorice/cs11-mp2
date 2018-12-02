import json, os

with open(os.path.join(os.path.dirname(__file__), 'config.json')) as f:
    config = json.load(f)

class Card():
    """
    This class is used to store information about the card during the game's runtime.

    Args:
        card_id (int): The unique identifying number of card.
        card_key (int): The key that corresponds to the `config.json` on which card information will be used.
    
    Attributes:
        id (int): The unique identifying number of card.
        content (str): The "face" of the card in string form, in order to check if two cards match
            during the game's runtime.
        correct (bool): This determines if the card has already been correctly guessed.
        flipped (bool): This determines if the card is face up or is face down.
        flipping (int): The flipping state of the card, it determines card animation when flipping, and is used by
            the interface during the calculation of the animations.
        healing (bool): This determines if the card is a potion, and adds 1 to the Player's health when
            correctly matched.
        img_url (str): This points to the file of the corresponding card face image to be used.
        key (int): The key that corresponds to the `config.json` on which card information will be used.
    """
    def __init__(self, card_id, card_key):
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
