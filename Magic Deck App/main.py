from __future__ import division

import math
import textwrap

from lib import deck

from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

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

        self.background = Image(allow_stretch=True, source="")
        self.add_widget(self.background)
        self.load_image()

    def load_image(self):
        image = CardGameApp.CardPath+self.card.Filename()
        self.background.source = image
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


class CardMat(FloatLayout):
    def __init__(self, **kwargs):
        super(CardMat, self).__init__(**kwargs)
        self.__dict__.update(kwargs)

        # Draw and hook up a quit button
        quit = Button(pos=(CardGameApp.Border, CardGameApp.Border),
                      size_hint=(.06, .04), text="Quit")
        quit.bind(on_press=app.Quit)
        self.add_widget(quit)

        self.widget_view = Button(text="Change to Grid")
        self.widget_view.bind(on_release=self.do_change_view)

        # ## #

        self.widget_strip = BoxLayout(
          pos=(CardGameApp.Border, CardGameApp.Border),
          pos_hint={'x': .2}, size_hint=(.8, .04))

        self.widget_deckorders = DropDown()
        for name, order in deck.ORDERS.items():
            btn = Button(text=name, size_hint_y=None, height=22)
            btn.bind(on_release=self.sort_deck)
            self.widget_deckorders.add_widget(btn)
        self.widget_deckordersbtn = Button(text='Deck Orders')
        self.widget_deckordersbtn.bind(on_release=self.widget_deckorders.open)
        self.widget_strip.add_widget(self.widget_deckordersbtn)

        export = Button(
            pos=(CardGameApp.Border, CardGameApp.Border), text="Export")
        export.bind(on_release=self.export_deck)
        self.widget_strip.add_widget(export)

        import_deckorder = Button(
            pos=(CardGameApp.Border, CardGameApp.Border), text="Import")
        import_deckorder.bind(on_release=self.import_deck)
        self.widget_strip.add_widget(import_deckorder)

        cut = Button(pos=(CardGameApp.Border, CardGameApp.Border), text="Cut")
        cut.bind(on_release=self.cut)
        self.widget_strip.add_widget(cut)

        # ## #

        self.widget_shuffle = DropDown()

        antifaro = Button(size_hint_y=None, height=22, text="Anti-Faro")
        antifaro.bind(on_release=self.anti_faro)
        self.widget_shuffle.add_widget(antifaro)

        infaro = Button(size_hint_y=None, height=22, text="In-Faro")
        infaro.bind(on_release=self.in_faro)
        self.widget_shuffle.add_widget(infaro)

        outfaro = Button(size_hint_y=None, height=22, text="Out-Faro")
        outfaro.bind(on_release=self.out_faro)
        self.widget_shuffle.add_widget(outfaro)

        riffle = Button(size_hint_y=None, height=22, text="Riffle")
        riffle.bind(on_release=self.riffle)
        self.widget_shuffle.add_widget(riffle)

        wash = Button(size_hint_y=None, height=22, text="Wash")
        wash.bind(on_release=self.wash)
        self.widget_shuffle.add_widget(wash)

        self.widget_shufflebtn = Button(text='Shuffle...')
        self.widget_shufflebtn.bind(on_release=self.widget_shuffle.open)
        self.widget_strip.add_widget(self.widget_shufflebtn)

        self.widget_strip.add_widget(self.widget_view)
        self.add_widget(self.widget_strip)
        self.update_strip()

    def create_cards(self):
        self.cards = []
        for i in range(0, len(self.deck.cards)):
            card = CardWidget(card=self.deck.cards[i], layout=self)
            self.cards.append(card)
            self.add_widget(card)
        self.render()

    def sort_deck(self, btn):
        self.deck.create_deck_from(deck.ORDERS[btn.text])

        for card in self.cards:
            self.remove_widget(card)
        self.create_cards()

    def export_deck(self, btn):
        str = self.deck.return_deckstring()
        Popup(title='Deck String',
              content=TextInput(text=str,
                                padding=[20, 20, 20, 20],
                                readonly=True),
              size_hint=(None, None), size=(300, 300)).open()

    def import_deck(self, btn):
        ti = TextInput(text="", padding=[20, 20, 20, 20])
        btn = Button(text="Import")

        layout = BoxLayout()
        layout.add_widget(ti)
        layout.add_widget(btn)

        popup = Popup(title='Please enter the deck string.',
                      content=layout,
                      size_hint=(None, None), size=(300, 300))
        btn.bind(on_release=lambda btn: self.load_deck(popup, ti.text))
        popup.open()

    def load_deck(self, popup, deck_string):
        try:
            self.deck.create_deck_from(deck_string)
        except IndexError:
            Popup(title='Load Deck Failed!',
                  content=Label(text="Invalid deck string!"),
                  size_hint=(None, None), size=(200, 100)).open()
            return
        except ValueError:
            Popup(title='Load Deck Failed!',
                  content=Label(text="Invalid deck string!"),
                  size_hint=(None, None), size=(200, 100)).open()
            return

        popup.dismiss()
        for card in self.cards:
            self.remove_widget(card)
        self.create_cards()

    def in_faro(self, btn):
        self.deck.infaro()

        for card in self.cards:
            self.remove_widget(card)
        self.create_cards()

    def out_faro(self, btn):
        self.deck.outfaro()

        for card in self.cards:
            self.remove_widget(card)
        self.create_cards()

    def anti_faro(self, btn):
        self.deck.antifaro()

        for card in self.cards:
            self.remove_widget(card)
        self.create_cards()

    def riffle(self, btn):
        self.deck.riffle()

        for card in self.cards:
            self.remove_widget(card)
        self.create_cards()

    def wash(self, btn):
        self.deck.shuffle()

        for card in self.cards:
            self.remove_widget(card)
        self.create_cards()

    def cut(self, btn):
        ti = TextInput(text="26", multiline=False)
        btn = Button(text="Submit")

        layout = BoxLayout()
        layout.add_widget(ti)
        layout.add_widget(btn)

        popup = Popup(title='Cut at what location?',
                      content=layout,
                      size_hint=(None, None), size=(200, 100))
        btn.bind(on_release=lambda btn: self.complete_cut(popup, ti.text))
        popup.open()

    def complete_cut(self, popup, location):
        popup.dismiss()
        self.deck.cut(int(location))

        for card in self.cards:
            self.remove_widget(card)
        self.create_cards()

    def render(self):
        if CardGameApp.OverlappingCards:
            # Render all cards in deck using overlapping positions
            self.render_fan()
        else:
            self.render_grid()
            # Render all cards in deck using gridded positions

    def render_fan(self):
        """
        Attempt to create a radial fan of all the cards
        """
        count = len(self.deck.cards)
        unit = (1 - CardGameApp.Border) / (count/3.5)
        r = .6

        for i in range(0, count):
            self.cards[i].size_hint = (unit, unit*CardGameApp.CardHeightRatio)
            angle = (count - i) * (math.pi/2) / count + .76

            self.cards[i].pos_hint = {
              'x': CardGameApp.Border + math.cos(angle)*r + .46,
              'top': 1 - CardGameApp.Border + math.sin(angle)*r - .9
            }

    def render_grid(self):
        unit = (1 - CardGameApp.Border) / CardGameApp.CardsPerRow
        height = unit * CardGameApp.CardHeightRatio

        for i in range(0, len(self.deck.cards)):
            row = math.floor(i / CardGameApp.CardsPerRow)
            self.cards[i].pos_hint = {
                'x': .002 + unit * (i % CardGameApp.CardsPerRow),
                'top': 1 - CardGameApp.Border - (height*row)}
            self.cards[i].size_hint = (unit, unit*CardGameApp.CardHeightRatio)

    def do_change_view(self, instance):
        if CardGameApp.OverlappingCards:
            CardGameApp.OverlappingCards = False
        else:
            CardGameApp.OverlappingCards = True

        self.update_strip()
        self.render()

    def update_strip(self):
        if CardGameApp.OverlappingCards:
            self.widget_view.text = "View as Grid"
        else:
            self.widget_view.text = "View Fanned"


class CardGameApp(App):
    # Config: Percentage of padding around all elements
    Border = .005

    # Config: Where can we find card images?
    CardPath = "images/card/default/"

    # Config: How many cards to draw per row?
    CardsPerRow = 13

    # Config: If cards should be drawn "overlapped" (fanned) or individually
    OverlappingCards = True

    # Config: What is the ratio of height to width of a playing card?
    PlayingCardRatio = 1.55

    # static method
    def Resize(window, width, height):
        """
        widget event receiver for `on_resize` that adjusts card display ratio
        """
        CardGameApp.DisplayRatio = Window.size[0] / Window.size[1]

        # make sure cards are drawn with the correct height to width ratio
        CardGameApp.CardHeightRatio = CardGameApp.DisplayRatio * CardGameApp.PlayingCardRatio

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
        Window.bind(on_resize=CardGameApp.Resize)
        Window.size = (1280, 720)

        # Primary Logic
        self.deck = deck.Deck()
        root = CardMat(deck=self.deck, do_rotation=False, do_scale=False)
        root.create_cards()
        return root


# in case we need global access
app = None

if __name__ == '__main__':
    app = CardGameApp()
    app.run()
