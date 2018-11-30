import pyglet, datetime, time

# Logging functions:

def log(string, logged=True):
    if not logged:
        return
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

# Program logic:

class Interface():
    def __init__(self):
        """This instantiates the Interface() class."""
        log("[-RUN-] Fetching assets...")
        pyglet.resource.path = ['assets/', 'assets/cards']
        pyglet.resource.reindex()
        self.sprites = []
        self.click_listeners = []
        self.is_picking = False
        self.flipped_cards = []
        self.delay = [False, 0, 0]

    def update(self, dt):
        self.card_render()
        for sprite in self.sprites:
            sprite.draw()

        if self.delay[0]:
            self.delay[1] +=1
            if self.delay[1] >= self.delay[2]:
                self.delay = [False, 0, 0]
                for card in self.flipped_cards:
                    card.flip()
                self.flipped_cards = []

    def card_render(self):
        self.click_listeners = []
        self.sprites = []
        i = 0
        for card in self.board.cards:
            current_row = i % self.board.rows
            current_col = i // self.board.rows
            if not card.flipped:
                card_image = pyglet.resource.image("card_back.png")
            else:
                card_image = pyglet.resource.image(card.img_url)
            card_image.width = self.card_size
            card_image.height = self.card_size
            card_image.anchor_x = 0
            card_image.anchor_y = 0

            # calculate position of card, with spacing
            x_pos = (current_row*self.card_size + (self.spacing*current_row))+self.offset['x']
            y_pos = (current_col*self.card_size + (self.spacing*current_col))+self.offset['y']

            # adds a listener, ((x1, x2), (y1, y2))
            if not card.correct:
                listener = ((x_pos, x_pos+self.card_size), (y_pos, y_pos+self.card_size), card)
                self.click_listeners.append(listener)

            card_sprite = pyglet.sprite.Sprite(card_image, x=x_pos, y=y_pos)
            self.sprites.append(card_sprite)
            i += 1

    def start_game(self, board, player):
        """
        This function starts the game.
        
        Args:
            board (Board): board.Board() object to render.
        """

        self.board = board
        self.player = player

        window = pyglet.window.Window(width=1280, height=720)
        card_count = len(board.cards)
        # computation: raw card size * cards + raw spacing size * cards-1
        raw_full_height = (board.cols * 512) + ((board.cols-1) * 64)
        # map raw height to 700 px:
        height_offset = 590/raw_full_height
        self.card_size, self.spacing = int(512*height_offset), int(64*height_offset)
        real_width = (self.card_size*board.rows) + (self.spacing*(board.rows-1))
        self.offset = {'x':(1280-real_width)//2, 'y':50}

        label = pyglet.text.Label(
            "Hello, world",
            font_name="Times New Roman",
            font_size=36,
            x=window.width//2, y=window.height//2,
            anchor_x="center", anchor_y="center"
        )

        @window.event
        def on_draw():
            # clears the window:
            window.clear()

            label.draw()
            self.card_render()
            for sprite in self.sprites:
                sprite.draw()

            if self.delay[0]:
                self.delay[1] +=1
                if self.delay[1] >= self.delay[2]:
                    self.delay = [False, 0, 0]
                    for card in self.flipped_cards:
                        card.flip()
                    self.flipped_cards = []

        @window.event
        def on_mouse_press(x, y, button, modifiers):
            if self.delay[0]:
                return
            if button != pyglet.window.mouse.LEFT:
                return
            for listener in self.click_listeners:
                if (
                    listener[0][0] <= x <= listener[0][1]
                ) and (
                    listener[1][0] <= y <= listener[1][1]
                ):
                    listener[2].flip()
                    self.card_render()
                    for sprite in self.sprites:
                        sprite.draw()
                    if self.is_picking:
                        if listener[2].content == self.flipped_cards[0].content:
                            listener[2].set_correct()
                            self.flipped_cards[0].set_correct()
                            self.flipped_cards = []
                            self.player.score += 1
                        else:
                            self.flipped_cards.append(listener[2])
                            self.delay = [True, 0, 45]
                    else:
                        self.flipped_cards.append(listener[2])
                    self.is_picking = not self.is_picking
