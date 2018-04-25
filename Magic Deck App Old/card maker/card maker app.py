from __future__ import division

import os, os.path
import math
import random
import sys
import time
import textwrap

from lib.deck import Deck # /lib/deck.py:Deck

from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from PIL import Image, ImageDraw, ImageFont

# graphics configuration must come before importing Window
# Config.set('graphics', 'fullscreen', 'auto')

# Simulates fullscreen without really going there
Config.set('graphics', 'borderless', 1)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'top', 0)
Config.set('graphics', 'left', 0)

# We can make a card game pretty
Config.set('graphics', 'maxfps', 30)
Config.set('graphics', 'multisamples', 16)

from kivy.app import App
from kivy.core.window import Window   # ignore warning E402

CARD_DIMENSION = (736, 1024)
CARD_PADDING = 16

# Font = ImageFont.truetype('fonts/open-sans/OpenSans-Regular.ttf', 99) # font size

def create_image(card, filename="image1.png", card_type="bicycle"):
    card_type = card_type.lower()
    img_w, img_h = CARD_DIMENSION
    p = CARD_PADDING

    im = Image.new("RGBA", (img_w, img_h), color=(255, 255, 255, 255))
    if card_type == "bicycle":
        fg = Image.open("card_images/{a}.png".format(a=card.value.upper()))
        sz = fg.size
        im.paste(fg, (p, p)) # top left
        im.paste(fg.rotate(180), (img_w - sz[0] - p - p, img_h - sz[1] - p - p)) # bottom right
        fg = Image.open("card_images/{b}.png".format(b=card.suit.upper()))
        sz2 = fg.size
        im.paste(fg, (p, p + p + sz[1])) # top left
        im.paste(fg.rotate(180), (img_w - sz[0] - p - p, img_h - sz[1] - sz2[1] - p - p - p)) # bottom right

    elif card_type == "index":
        fg = Image.open("card_images/{a}.png".format(a=card.value.upper()))
        sz = fg.size
        sz = (sz[0]*4, sz[1]*4)
        fg = fg.resize(sz, Image.ANTIALIAS)
        im.paste(fg, (int(img_w / 2), p))

        fg = Image.open("card_images/{b}.png".format(b=card.suit.upper()))
        sz = fg.size
        sz = (sz[0]*4, sz[1]*4)
        fg = fg.resize(sz, Image.ANTIALIAS)
        im.paste(fg, (int(img_w / 2), p + sz[0] + p)) # under top middle

    else:
        raise TypeError("Inappropriate Card Type: \"{type}\"".format(type=card_type))

    im.save(filename)
    return True


class CardWidget(Button):
    def __init__(self, **kwargs):
        super(CardWidget, self).__init__(**kwargs)
        self.__dict__.update(kwargs)

        self.text = textwrap.fill(self.card.__str__(), 10)

        self.bind(on_touch_down=self.do_touch_down)
        self.bind(on_touch_move=self.do_touch_move)
        self.bind(on_touch_up=self.do_touch_up)
        self.bind(pos=self.update)
        self.bind(on_press=self.do_press)

        self.background_color = [1, 1, 1, 1]
        self.background_normal = ''
        self.selected = False
        self.move_started = False

        self.background = KivyImage(allow_stretch=True, source="")
        self.add_widget(self.background)
        self.load_image()

    def load_image(self):
        fn = CardMakerApp.CardPath + "new/" + self.card.filename()
        create_image(self.card, filename=fn, card_type=CardMakerApp.CardType)
        self.background.source = fn
        self.background.reload()

    def update(self, instance, pos):
        self.background.pos = (
            self.pos[0] + 4,
            self.pos[1])
        self.background.size = (
            self.size[0] - 8,
            self.size[1])

    def do_touch_down(self, instance, touch):
        if self.collide_point(*touch.pos):
            x = touch.pos[0] - self.pos[0]
            y = touch.pos[1] - self.pos[1]
            self.move_offset = [x, y]
            self.move_started = True

            # Force "on top"
            self.layout.remove_widget(self)
            self.layout.add_widget(self)
        return super(Button, self).on_touch_down(touch)

    def do_touch_move(self, instance, touch):
        if self.move_started:
            self.pos[0] = touch.pos[0] - self.move_offset[0]
            self.pos[1] = touch.pos[1] - self.move_offset[1]
            self.pos_hint = {}  # Kill automatic layout
        return super(Button, self).on_touch_move(touch)

    def do_touch_up(self, instance, touch):
        if self.move_started:
            self.pos[0] = touch.pos[0] - self.move_offset[0]
            self.pos[1] = touch.pos[1] - self.move_offset[1]
            self.move_started = False
        return super(Button, self).on_touch_up(touch)

    def do_press(self, instance):
        if self.selected:
            self.selected = False
            self.background_color = [1, 1, 1, 1]
        else:
            self.selected = True
            self.background_color = [.5, .5, 1, 1]


class CardMaker(FloatLayout):
    def __init__(self, **kwargs):
        super(CardMaker, self).__init__(**kwargs)
        self.__dict__.update(kwargs)

        # Draw and hook up a quit button
        quit = Button(pos=(CardMakerApp.Border, CardMakerApp.Border),
                      size_hint=(.06, .04), text="Quit")
        quit.bind(on_press=app.Quit)
        self.add_widget(quit)

    def create_cards(self):
        self.cards = []
        for i in range(0, len(self.deck.cards)):
            card = CardWidget(card=self.deck.cards[i], layout=self)
            self.cards.append(card)
            self.add_widget(card)
        self.render()

    def render(self):
        count = len(self.deck.cards)
        unit = (1 - CardMakerApp.Border) / (count/3.5)
        r = .6

        for i in range(0, count):
            self.cards[i].size_hint = (unit, unit*CardMakerApp.CardHeightRatio)
            angle = (count - i) * (math.pi/2) / count + .76

            self.cards[i].pos_hint = {
              'x': CardMakerApp.Border + math.cos(angle)*r + .46,
              'top': 1 - CardMakerApp.Border + math.sin(angle)*r - .9
            }


class CardMakerApp(App):
    # Config: Percentage of padding around all elements
    Border = .005

    # Config: Where can we find card images?
    CardPath = "card_images/"

    # Config: Type of card to be created
    CardType = "Bicycle"

    # Config: What is the ratio of height to width of a playing card?
    PlayingCardRatio = 1.55

    # static method
    def Resize(window, width, height):
        """
        widget event receiver for `on_resize` that adjusts card display ratio
        """
        CardMakerApp.DisplayRatio = Window.size[0] / Window.size[1]

        # make sure cards are drawn with the correct height to width ratio
        CardMakerApp.CardHeightRatio = CardMakerApp.DisplayRatio * CardMakerApp.PlayingCardRatio

    def Quit(window):
        """
        widget event receiver that exits the program
        """
        app.stop()

    def build(self):
        """
        instance method (from App)
        """
        # Set resolution, windowed or fullscreen (careful!)
        #   if the resoultion can't be displayed, we won't know!
        Window.bind(on_resize=CardMakerApp.Resize)
        Window.size = (1280, 720)

        # Deck Preparations
        self.deck = Deck()
        self.deck.make_new_deck_order()
        for card in self.deck.cards:
            print str(card)

        # root = our main program window
        root = CardMaker(deck=self.deck, do_rotation=False, do_scale=False)
        root.create_cards()
        return root


# in case we need global access
app = None

if __name__ == '__main__':
    app = CardMakerApp()
    app.run()
