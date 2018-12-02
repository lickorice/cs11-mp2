import pyglet, datetime, time, random
from modules import engine as e
from modules import player as p
from modules import button as btn

class Interface():
    def __init__(self):
        """This instantiates the Interface() class."""
        pyglet.resource.path = ['assets/anims', 'assets/text', 'assets/btns', 'assets/bgs', 'assets/cards']
        pyglet.resource.reindex()
        self.window = pyglet.window.Window(width=1280, height=720)
        self.sprites = []
        self.click_listeners = []
        self.bgs = []
        self.is_picking = False
        self.flipped_cards = []
        self.delay = [False, 0, 0]
        self.card_delay = [False, 0, 0, ""]
        self.engine = e.Engine()

        self.game_is_running = False
        self.menu_is_running = True
        self.coin_counter = 0
        self.bg_counter = 0
        self.bg_d_counter = 0
        
        self.current_anims = {}
        self.flip_in = ["card_flip0{}.png".format(i) for i in range(5)]
        self.flip_out = ["card_flip1{}.png".format(i) for i in range(5)]

        play_button = btn.Button()
        settings_button = btn.Button()
        quit_button = btn.Button()

        self.batch = pyglet.graphics.Batch()
        self.bg = pyglet.graphics.OrderedGroup(0)
        self.fg = pyglet.graphics.OrderedGroup(1)

        self.level = 1
        self.card_count = 2

        pyglet.font.add_file('assets/text/pixel_regular.ttf')
        self.pixel_regular = pyglet.font.load('Perfect DOS VGA 437 Win')

        self.menu_buttons = [play_button, settings_button, quit_button]
        self.back_button = btn.Button()
        self.music_player = pyglet.media.Player()
        self.menu_music = pyglet.media.load("assets/audio/bgm_menu.wav")
        self.click_sound = pyglet.media.load("assets/audio/fx_click.wav", streaming=False)
        self.flip_sound = pyglet.media.load("assets/audio/fx_flip.wav", streaming=False)
        self.all_done_sound = pyglet.media.load("assets/audio/fx_all_done.wav", streaming=False)
        self.correct_sound = pyglet.media.load("assets/audio/fx_correct.wav", streaming=False)
        self.wrong_sound = pyglet.media.load("assets/audio/fx_wrong.wav", streaming=False)
        self.heal_sound = pyglet.media.load("assets/audio/fx_heal.wav", streaming=False)

    def load_bg_menu(self):
        if not self.menu_is_running:
            return
        # bg_image = pyglet.resource.image(self.bg_images["menu"][self.bg_counter])
        bg_image = pyglet.resource.image("menu_bg.png")
        text_image = pyglet.resource.image("title.png")
        text_image.anchor_x = text_image.width//2
        bg_sprite = pyglet.sprite.Sprite(bg_image, (self.bg_counter/500)*-1280, (self.bg_counter/500)*-720, batch=self.batch, group=self.bg)
        text_sprite = pyglet.sprite.Sprite(text_image, 640, 500, batch=self.batch, group=self.fg)
        self.sprites.append(bg_sprite)
        self.sprites.append(text_sprite)
        self.bg_counter = (self.bg_counter + 1) % 500
    
    def load_bg_scoreboard(self):
        if not self.scoreboard_is_running:
            return
        bg_image = pyglet.resource.image("menu_bg.png")
        bg_sprite = pyglet.sprite.Sprite(bg_image, (self.bg_counter/500)*-1280, (self.bg_counter/500)*-720, batch=self.batch, group=self.bg)
        self.sprites.append(bg_sprite)
        self.bg_counter = (self.bg_counter + 1) % 500

        if self.back_button.hovering:
            back_image = pyglet.resource.image("btn_back1.png")
        else:
            back_image = pyglet.resource.image("btn_back0.png")

        back_image.width = 70
        back_image.height = 70

        back_sprite = pyglet.sprite.Sprite(back_image, 20, 650, batch=self.batch, group=self.fg)

        self.back_button.x_range = (20, 90)
        self.back_button.y_range = (650, 720)

        listener = (
                self.back_button.x_range,
                self.back_button.y_range,
                self.start_menu,
                "back2"
            )
        self.sprites.append(back_sprite)
        self.click_listeners.append(listener)

    def load_bg_score(self):
        if not self.score_is_running:
            return
        # bg_image = pyglet.resource.image(self.bg_images["menu"][self.bg_counter])
        bg_image = pyglet.resource.image("menu_bg.png")
        line_image = pyglet.resource.image("name_line.png")
        line_image.anchor_x = line_image.width//2
        bg_sprite = pyglet.sprite.Sprite(bg_image, (self.bg_counter/500)*-1280, (self.bg_counter/500)*-720, batch=self.batch, group=self.bg)
        line_sprite = pyglet.sprite.Sprite(line_image, 640, 300, batch=self.batch, group=self.fg)
        self.sprites.append(bg_sprite)
        self.sprites.append(line_sprite)
        self.bg_counter = (self.bg_counter + 1) % 500

    def load_bg_dung(self):
        if not self.game_is_running:
            return
        # bg_image = pyglet.resource.image(self.bg_images["dung"][self.bg_d_counter])
        bg_image = pyglet.resource.image("dungeon_bg.png")
        coin_image = pyglet.resource.image("coin%02d.png"%(self.coin_counter//4))
        heart_image = pyglet.resource.image("heart.png")
        heart_image.anchor_x = heart_image.width
        bg_sprite = pyglet.sprite.Sprite(bg_image, (self.bg_d_counter/500)*-1280, (self.bg_d_counter/500)*-720, batch=self.batch, group=self.bg)
        coin_sprite = pyglet.sprite.Sprite(coin_image, 20, 20, batch=self.batch, group=self.fg)
        for i in range(self.player.health):
            heart_sprite = pyglet.sprite.Sprite(heart_image, 1260 - ((heart_image.width+5)*i), 20, batch=self.batch, group=self.fg)
            self.sprites.append(heart_sprite)
        self.sprites.append(bg_sprite)
        self.sprites.append(coin_sprite)
        self.coin_counter = (self.coin_counter + 1) % 64
        self.bg_d_counter = (self.bg_d_counter + 1) % 500

        if self.back_button.hovering:
            back_image = pyglet.resource.image("btn_back1.png")
        else:
            back_image = pyglet.resource.image("btn_back0.png")

        back_sprite = pyglet.sprite.Sprite(back_image, 20, 600, batch=self.batch, group=self.fg)

        self.back_button.x_range = (20, 100)
        self.back_button.y_range = (600, 720)

        listener = (
                self.back_button.x_range,
                self.back_button.y_range,
                self.start_menu,
                "back"
            )
        self.sprites.append(back_sprite)
        self.click_listeners.append(listener)

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
            if not card.flipped:
                listener = ((x_pos, x_pos+self.card_size), (y_pos, y_pos+self.card_size), card, "card")
                self.click_listeners.append(listener)

            card_sprite = pyglet.sprite.Sprite(card_image, x=x_pos, y=y_pos, batch=self.batch, group=self.fg)
            self.sprites.append(card_sprite)
            i += 1
    
    def btn_render(self):
        if self.score_is_running:
            if self.menu_buttons[0].hovering:
                submit_image = pyglet.resource.image("btn_submit1.png")
            else:
                submit_image = pyglet.resource.image("btn_submit0.png")
            submit_image.anchor_x = submit_image.width//2
            submit_sprite = pyglet.sprite.Sprite(submit_image, 640, 150, batch=self.batch, group=self.fg)

            self.sprites.append(submit_sprite)
            self.menu_buttons[0].x_range = (640-submit_image.width//2, 640+submit_image.width//2)
            self.menu_buttons[0].y_range = (150, 150+submit_image.height)

            listener = (
                self.menu_buttons[0].x_range,
                self.menu_buttons[0].y_range,
                self.start_menu,
                "submit"
            )

            self.click_listeners.append(listener)

        elif self.menu_is_running:
            if self.menu_buttons[0].hovering:
                play_image = pyglet.resource.image("btn_play1.png")
            else:
                play_image = pyglet.resource.image("btn_play0.png")
            play_image.anchor_x = play_image.width//2
            play_sprite = pyglet.sprite.Sprite(play_image, 640, 300, batch=self.batch, group=self.fg)

            if self.menu_buttons[1].hovering:
                settings_image = pyglet.resource.image("btn_settings1.png")
            else:
                settings_image = pyglet.resource.image("btn_settings0.png")
            settings_image.anchor_x = settings_image.width//2
            settings_sprite = pyglet.sprite.Sprite(settings_image, 640, 200, batch=self.batch, group=self.fg)
            
            if self.menu_buttons[2].hovering:
                quit_image = pyglet.resource.image("btn_quit1.png")
            else:
                quit_image = pyglet.resource.image("btn_quit0.png")
            quit_image.anchor_x = quit_image.width//2
            quit_sprite = pyglet.sprite.Sprite(quit_image, 640, 100, batch=self.batch, group=self.fg)

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
            listener = (
                self.menu_buttons[1].x_range,
                self.menu_buttons[1].y_range,
                self.start_scoreboard,
                "button"
            )
            self.click_listeners.append(listener)
            listener = (
                self.menu_buttons[2].x_range,
                self.menu_buttons[2].y_range,
                self.quit,
                "button"
            )
            self.click_listeners.append(listener)

    def transition(self):
        """This function provides a transition between games."""
        self.game_is_running = False
        self.level += 1
        self.transition_label = self.score_label = pyglet.text.Label(
            "LEVEL {}".format(self.level),
            font_size=36, x=640, y=360, font_name='Perfect DOS VGA 437 Win',
            batch=self.batch, group=self.fg, anchor_x="center", anchor_y="center"
            )
        if self.card_count < 32:
            self.card_count *=2
        self.delay = [True, 0, 60, "transition"]

    def start_scoreboard(self, *args, **kwargs):
        """This function opens up the scoreboard."""

        self.scoreboard_is_running = True
        self.game_is_running = False
        self.menu_is_running = False
        self.score_is_running = False

        self.sprites = []
        self.click_listeners = []

        self.scoreboard = self.engine.get_scoreboard()
        
        self.scoreboard_text = []

        title_label = pyglet.text.Label(
                "Top 10 Players",
                anchor_x = "center", anchor_y = "center",
                font_name='Perfect DOS VGA 437 Win',
                font_size=100,
                batch=self.batch, group=self.fg,
                x=640, y=600
            )

        name_label = pyglet.text.Label(
                "NAME",
                anchor_x = "center", anchor_y = "center",
                font_name='Perfect DOS VGA 437 Win',
                font_size=50,
                batch=self.batch, group=self.fg,
                x=320, y=500
            )

        score_label = pyglet.text.Label(
                "SCORE",
                anchor_x = "center", anchor_y = "center",
                font_name='Perfect DOS VGA 437 Win',
                font_size=50,
                batch=self.batch, group=self.fg,
                x=640, y=500
            )

        level_label = pyglet.text.Label(
                "LEVEL",
                anchor_x = "center", anchor_y = "center",
                font_name='Perfect DOS VGA 437 Win',
                font_size=50,
                batch=self.batch, group=self.fg,
                x=960, y=500
            )

        self.scoreboard_text.append(title_label)
        self.scoreboard_text.append(name_label)
        self.scoreboard_text.append(score_label)
        self.scoreboard_text.append(level_label)

        i = 0
        for player in self.scoreboard:
            label = pyglet.text.Label(
                str(player.score),
                anchor_x = "center", anchor_y = "center",
                font_name='Perfect DOS VGA 437 Win',
                font_size=30,
                batch=self.batch, group=self.fg,
                x=640, y=440-(i*32)
            )
            self.scoreboard_text.append(label)
            label = pyglet.text.Label(
                str(player.level),
                anchor_x = "center", anchor_y = "center",
                font_name='Perfect DOS VGA 437 Win',
                font_size=30,
                batch=self.batch, group=self.fg,
                x=960, y=440-(i*32)
            )
            self.scoreboard_text.append(label)
            label = pyglet.text.Label(
                player.name,
                anchor_x = "center", anchor_y = "center",
                font_name='Perfect DOS VGA 437 Win',
                font_size=30,
                batch=self.batch, group=self.fg,
                x=320, y=440-(i*32)
            )
            self.scoreboard_text.append(label)

            i += 1

    def start_menu(self):
        """This function opens up the main menu."""

        self.menu_is_running = True
        self.game_is_running = False
        self.score_is_running = False
        self.scoreboard_is_running = False
        
        self.is_picking = False
        self.card_count = 2
        self.level = 1
        self.flipped_cards = []
        self.sprites = []
        self.click_listeners = []

        music = pyglet.media.SourceGroup(self.menu_music.audio_format, None)
        music.loop = True
        try:
            music.queue(self.menu_music)
        except pyglet.media.exceptions.MediaException:
            pass
        self.music_player.queue(music)
        self.music_player.play()

    def start_game(self, board, player):
        """
        This function starts the game.
        
        Args:
            board (Board): board.Board() object to render.
        """

        self.game_is_running = True
        self.menu_is_running = False
        self.score_is_running = False
        self.scoreboard_is_running = False

        self.board = board
        self.player = player

        card_count = len(board.cards)
        # computation: raw card size * cards + raw spacing size * cards-1
        raw_full_height = (board.cols * 512) + ((board.cols-1) * 64)
        # map raw height to 700 px:
        height_offset = 460/raw_full_height
        self.card_size, self.spacing = int(512*height_offset), int(64*height_offset)
        real_width = (self.card_size*board.rows) + (self.spacing*(board.rows-1))
        self.offset = {'x':(1280-real_width)//2, 'y':140}

        self.score_label = pyglet.text.Label(str(self.player.score), font_size=72, x=140, y=30, font_name='Perfect DOS VGA 437 Win', batch=self.batch, group=self.fg)
        self.card_delay = [True, 0, 120, "starting"]

    def start_score(self, player):
        """
        This function shows the scoreboard.

        Args:
            player (Player): player.Player() object to be used for scoring.
        """

        self.score_is_running = True
        self.game_is_running = False
        self.menu_is_running = False

        score_phrases = ["Nice work!", "Good job!", "Congratulations!", "Awesome!"]
        random.shuffle(score_phrases)
        plurality = '' if player.score == 1 else 's'
        self.score_label = pyglet.text.Label(
            "{} You have achieved {} point{}!".format(score_phrases[0], player.score, plurality),
            font_size=36, x=640, y=500, font_name='Perfect DOS VGA 437 Win',
            batch=self.batch, group=self.fg, anchor_x = "center"
            )
        self.name_label = pyglet.text.Label(
            "Enter name".format(score_phrases[0], player.score, plurality),
            font_size=36, x=640, y=320, font_name='Perfect DOS VGA 437 Win',
            batch=self.batch, group=self.fg, anchor_x = "center"
            )

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
            self.load_bg_dung()
            self.load_bg_score()
            self.load_bg_scoreboard()
            self.btn_render()
            self.card_render()
            self.batch.draw()

            for anim in self.current_anims:
                self.current_anims[anim][0] += 1
                if self.current_anims[anim][0] >= 4:
                    self.current_anims[anim][1].flipping = 2

            if self.card_delay[0]:
                self.card_delay[1] +=1
                if self.card_delay[1] >= self.card_delay[2]:
                    if self.card_delay[3] == "starting":
                        for card in self.board.cards:
                            self.flip_card(card, audio=False)
                            card.flip()
                        self.flip_sound.play()
                    if self.card_delay[3] == "ending":
                        for card in self.board.cards:
                            self.flip_card(card, audio=False)
                            card.flip()
                        self.flip_sound.play()
                        self.delay = [True, 0, 15, "continue"]
                    self.card_delay = [False, 0, 0, ""]

            if self.delay[0]:
                self.delay[1] +=1
                if self.delay[1] >= self.delay[2]:
                    if self.delay[3] == "wrong":
                        for card in self.flipped_cards:
                            self.flip_card(card)
                            card.flip()
                        self.flipped_cards = []
                        self.delay = [False, 0, 0, ""]
                    elif self.delay[3] == "ending":
                        self.score_label.delete()
                        self.start_score(self.player)
                        self.delay = [False, 0, 0, ""]
                    elif self.delay[3] == "continue":
                        self.score_label.delete()
                        self.transition()
                    elif self.delay[3] == "transition":
                        self.transition_label.delete()
                        self.engine.generate_cards(self.card_count)
                        self.start_game(self.engine.board, self.player)
                        self.delay = [False, 0, 0, ""]

        @self.window.event
        def on_key_press(symbol, modifiers):
            if ((97 > symbol or 122 < symbol) and symbol != 65288) or not self.score_is_running:
                return
            if symbol == 65288:
                self.player.name = self.player.name[:-1]
            else:
                if len(self.player.name) < 16:
                    self.player.name += chr(symbol).upper()
            self.name_label.text = self.player.name

        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            if self.menu_is_running or self.score_is_running:
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
            elif self.game_is_running or self.scoreboard_is_running:
                if (
                        self.back_button.x_range[0] <= x <= self.back_button.x_range[1]
                    ) and (
                        self.back_button.y_range[0] <= y <= self.back_button.y_range[1]
                    ):
                    if not self.back_button.hovering:
                        self.click_sound.play()
                    self.back_button.hovering = True
                else:
                    self.back_button.hovering = False

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
                    if listener[3] == "back":
                        self.score_label.delete()
                        self.start_menu()
                    if listener[3] == "back2":
                        for label in self.scoreboard_text:
                            label.delete()
                        self.start_menu()
                    if listener[3] == "button":
                        self.engine.generate_cards(self.card_count)
                        player = p.Player("", len(self.engine.board.cards))
                        listener[2](self.engine.board, player)
                    elif listener[3] == "submit":

                        if len(self.player.name) == 0:
                            self.name_label.text = "Please enter a name. (Keyboard)"
                            return

                        self.engine.submit_to_scoreboard(
                            self.player.name,
                            self.level,
                            self.player.score
                        )

                        self.name_label.delete()
                        self.score_label.delete()
                        listener[2]()
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
                                self.player.score += self.level*2
                                self.score_label.text = str(self.player.score)

                                if current_card.healing:
                                    self.player.health += 1
                                    self.heal_sound.play()
                                else:
                                    self.correct_sound.play()

                                remaining_cards = len([1 for card in self.board.cards if not card.correct])
                                if remaining_cards == 0:
                                    self.all_done_sound.play()
                                    self.card_delay = [True, 0, 120, "ending"]
                            else:
                                self.flipped_cards.append(current_card)
                                self.player.health -= 1
                                if self.player.health == 0:
                                    self.flipped_cards = []
                                    self.all_done_sound.play()
                                    self.delay = [True, 0, 120, "ending"]
                                else:
                                    self.wrong_sound.play()
                                    self.delay = [True, 0, 45, "wrong"]
                        else:
                            self.flipped_cards.append(current_card)
                        self.is_picking = not self.is_picking
