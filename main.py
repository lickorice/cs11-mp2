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
    log("[-RUN-] Running game...")
    log("[-RUN-] Running main game instance...")
    screen = interface.Interface()
    engine = e.Engine()
    engine.generate_cards(16)
    player = p.Player("placeholder", len(engine.board.cards))
    screen.start_game(engine.board, player)
    pyglet.clock.schedule_interval(screen.update, 1/120.0)
    pyglet.app.run()

if __name__ == "__main__":
    main()