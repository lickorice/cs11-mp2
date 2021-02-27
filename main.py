"""
I didn't include the .pdf in this repository, by the way.
Try compiling it yourself.
"""

import pyglet, datetime
from modules import interface
from modules import engine as e
from modules import player as p

# Logging functions:

def log(string, logged=True):
    if not logged:
        return
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

# Program logic:

def main():
    """This function runs the game."""
    log("[-RUN-] Running game...")
    log("[-RUN-] Running main game instance...")
    screen = interface.Interface()
    engine = e.Engine()
    # player = p.Player("placeholder", len(engine.board.cards))
    screen.start_menu()
    # engine.generate_cards(16)
    # screen.start_game(engine.board, player)
    pyglet.clock.schedule(screen.update)
    pyglet.app.run()

if __name__ == "__main__":
    main()