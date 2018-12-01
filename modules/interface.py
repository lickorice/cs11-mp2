import pyglet, datetime, time
from modules import engine as e
from modules import player as p
from modules import button as btn

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
        pyglet.resource.path = ['assets/anims', 'assets/btns', 'assets/bgs', 'assets/cards']
        pyglet.resource.reindex()
        self.window = pyglet.window.Window(width=1280, height=720)
        self.sprites = []
        self.click_listeners = []
        self.bgs = []
        self.is_picking = False
        self.flipped_cards = []
        self.delay = [False, 0, 0]
        self.card_delay = [False, 0, 0]
        self.engine = e.Engine()

        self.game_is_running = False
        self.menu_is_running = True
        self.bg_images = {"menu":[]}
        self.bg_counter = 0
        self.bg_d_counter = 0
        self.bg_images["menu"] = ["bg_menu%03d.jpg" % i for i in range(241)]
        self.bg_images["dung"] = ["bg_dung%03d.jpg" % i for i in range(148)]
        
        self.current_anims = {}
        self.flip_in = ["card_flip0{}.png".format(i) for i in range(5)]
        self.flip_out = ["card_flip1{}.png".format(i) for i in range(5)]

        play_button = btn.Button()
        settings_button = btn.Button()
        quit_button = btn.Button()

        self.batch = pyglet.graphics.Batch()

        self.menu_buttons = [play_button, settings_button, quit_button]
        self.music_player = pyglet.media.Player()
        self.menu_music = pyglet.media.load("assets/audio/bgm_menu.wav")
        self.click_sound = pyglet.media.load("assets/audio/fx_click.wav", streaming=False)
        self.flip_sound = pyglet.media.load("assets/audio/fx_flip.wav", streaming=False)

    def card_render(self):
        if not self.game_is_running:
            return
        self.click_listeners = []
        self.sprites = []
        self.load_bg_dung()
        i = 0
        for card in self.board.cards:
            current_row = i % self.board.rows
            current_col = i // self.board.rows

            if card.flipping == 0:
                card_image = pyglet.resource.image(
                    self.flip_in[self.current_anims[card.id][0]]
                    )
            elif card.flipping == 1:
                card_image = pyglet.resource.image(
                    self.flip_out[self.current_anims[card.id][0]]
                    )
            elif not card.flipped:
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
                listener = ((x_pos, x_pos+self.card_size), (y_pos, y_pos+self.card_size), card, "card")
                self.click_listeners.append(listener)

            card_sprite = pyglet.sprite.Sprite(card_image, x=x_pos, y=y_pos, batch=self.batch)
            self.sprites.append(card_sprite)
            i += 1

    def start_menu(self):
        """This function opens up the main menu."""
        self.menu_is_running = True
        self.sprites = []
        self.click_listeners = []

        music = pyglet.media.SourceGroup(self.menu_music.audio_format, None)
        music.loop = True
        music.queue(self.menu_music)
        self.music_player.queue(music)
        self.music_player.play()

    def load_bg_menu(self):
        if not self.menu_is_running:
            return
        bg_image = pyglet.resource.image(self.bg_images["menu"][self.bg_counter])
        bg_sprite = pyglet.sprite.Sprite(bg_image, 0, 0, batch=self.batch)
        self.sprites.append(bg_sprite)
        self.bg_counter = (self.bg_counter + 1) % 240

    def load_bg_dung(self):
        if not self.game_is_running:
            return
        bg_image = pyglet.resource.image(self.bg_images["dung"][self.bg_d_counter])
        bg_sprite = pyglet.sprite.Sprite(bg_image, 0, 0, batch=self.batch)
        self.sprites.append(bg_sprite)
        self.bg_d_counter = (self.bg_d_counter + 1) % 147
    
    def btn_render(self):
        if not self.menu_is_running:
            return
        if self.menu_buttons[0].hovering:
            play_image = pyglet.resource.image("btn_play1.png")
        else:
            play_image = pyglet.resource.image("btn_play0.png")
        play_image.anchor_x = play_image.width//2
        play_sprite = pyglet.sprite.Sprite(play_image, 640, 300, batch=self.batch)

        if self.menu_buttons[1].hovering:
            settings_image = pyglet.resource.image("btn_settings1.png")
        else:
            settings_image = pyglet.resource.image("btn_settings0.png")
        settings_image.anchor_x = settings_image.width//2
        settings_sprite = pyglet.sprite.Sprite(settings_image, 640, 200, batch=self.batch)
        
        if self.menu_buttons[2].hovering:
            quit_image = pyglet.resource.image("btn_quit1.png")
        else:
            quit_image = pyglet.resource.image("btn_quit0.png")
        quit_image.anchor_x = quit_image.width//2
        quit_sprite = pyglet.sprite.Sprite(quit_image, 640, 100, batch=self.batch)

        self.sprites.append(play_sprite)
        self.sprites.append(settings_sprite)
        self.sprites.append(quit_sprite)

        self.menu_buttons[0].x_range = (640-play_image.width//2, 640+play_image.width//2)
        self.menu_buttons[1].x_range = (640-play_image.width//2, 640+play_image.width//2)
        self.menu_buttons[2].x_range = (640-play_image.width//2, 640+play_image.width//2)
        self.menu_buttons[0].y_range = (300, 300+play_image.height)
        self.menu_buttons[1].y_range = (200, 200+play_image.height)
        self.menu_buttons[2].y_range = (100, 100+play_image.height)
        listener = (
            self.menu_buttons[0].x_range,
            self.menu_buttons[0].y_range,
            self.start_game,
            "button"
        )
        self.click_listeners.append(listener)
        # add settings button here
        listener = (
            self.menu_buttons[2].x_range,
            self.menu_buttons[2].y_range,
            self.quit,
            "button"
        )
        self.click_listeners.append(listener)

    def start_game(self, board, player):
        """
        This function starts the game.
        
        Args:
            board (Board): board.Board() object to render.
        """

        self.game_is_running = True
        self.menu_is_running = False

        self.board = board
        self.player = player

        card_count = len(board.cards)
        # computation: raw card size * cards + raw spacing size * cards-1
        raw_full_height = (board.cols * 512) + ((board.cols-1) * 64)
        # map raw height to 700 px:
        height_offset = 480/raw_full_height
        self.card_size, self.spacing = int(512*height_offset), int(64*height_offset)
        real_width = (self.card_size*board.rows) + (self.spacing*(board.rows-1))
        self.offset = {'x':(1280-real_width)//2, 'y':120}

        self.card_delay = [True, 0, 120]

    def flip_card(self, card, audio=True):
        self.current_anims[card.id] = [0, card]
        if audio:
            self.flip_sound.play()

    def quit(self, *args, **kwargs):
        quit()

    def update(self, dt):
        """Contains the main event loops."""

        @self.window.event
        def on_draw():
            # clears the window:
            self.window.clear()
            self.sprites = []
            self.click_listeners = []

            self.load_bg_menu()
            # self.load_bg_dung()
            self.btn_render()
            self.card_render()
            # for sprite in self.sprites:
            #     sprite.draw()
            self.batch.draw()

            for anim in self.current_anims:
                self.current_anims[anim][0] += 1
                if self.current_anims[anim][0] >= 4:
                    self.current_anims[anim][1].flipping = 2

            if self.card_delay[0]:
                self.card_delay[1] +=1
                if self.card_delay[1] >= self.card_delay[2]:
                    self.card_delay = [False, 0, 0]
                    for card in self.board.cards:
                        self.flip_card(card, audio=False)
                        card.flip()
                    self.flip_sound.play()

            if self.delay[0]:
                self.delay[1] +=1
                if self.delay[1] >= self.delay[2]:
                    self.delay = [False, 0, 0]
                    for card in self.flipped_cards:
                        self.flip_card(card)
                        card.flip()
                    self.flipped_cards = []

        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            if self.menu_is_running:
                for button in self.menu_buttons:
                    if (
                        button.x_range[0] <= x <= button.x_range[1]
                    ) and (
                        button.y_range[0] <= y <= button.y_range[1]
                    ):
                        if not button.hovering:
                            self.click_sound.play()
                        button.hovering = True
                    else:
                        button.hovering = False

        @self.window.event
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
                    if listener[3] == "button":
                        self.engine.generate_cards(100)
                        player = p.Player("nigger", len(self.engine.board.cards))
                        listener[2](self.engine.board, player)
                    elif listener[3] == "card":
                        current_card = listener[2]
                        current_card.flip()
                        self.flip_card(current_card)
                        self.card_render()
                        for sprite in self.sprites:
                            sprite.draw()
                        if self.is_picking:
                            if current_card.content == self.flipped_cards[0].content:
                                current_card.set_correct()
                                self.flipped_cards[0].set_correct()
                                self.flipped_cards = []
                                self.player.score += 1
                            else:
                                self.flipped_cards.append(current_card)
                                self.delay = [True, 0, 45]
                        else:
                            self.flipped_cards.append(current_card)
                        self.is_picking = not self.is_picking
