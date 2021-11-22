#
# Globals
#

deck = None
hands = []
text_edit = None

# Imports go Here

from deck import Deck
from card import Card
from hand import Hand

import pygame
from pygame.locals import *  ## Imports lots of stuff we don't need

## Gui Library Imports

import math, glob

from gui import *

# create the view, ie the tree of widgets
def create_widgets():

    global text_edit

    frame = Frame()
    frame.x = 200
    frame.y = 500
    frame.width = 625
    frame.height = 200

    button = Button(frame, ident="new_btn", text="New")
    button.x = 225
    button.y = 520
    button.width = 130
    button.height = 40

    button = Button(frame, ident="save_btn", text="Save")
    button.x = 225
    button.y = 560
    button.width = 130
    button.height = 40

    button = Button(frame, ident="load_btn", text="Load")
    button.x = 225
    button.y = 600
    button.width = 130
    button.height = 40

    button = Button(frame, ident="clear_btn", text="Clear")
    button.x = 225
    button.y = 640
    button.width = 130
    button.height = 40

    button = Button(frame, ident="faro_btn", text="Faro")
    button.x = 375
    button.y = 520
    button.width = 130
    button.height = 40

    button = Button(frame, ident="antifaro_btn", text="Antifaro")
    button.x = 375
    button.y = 560
    button.width = 130
    button.height = 40

    button = Button(frame, ident="cut_btn", text="Cut")
    button.x = 375
    button.y = 600
    button.width = 130
    button.height = 40

    button = Button(frame, ident="riffle_btn", text="Riffle")
    button.x = 525
    button.y = 520
    button.width = 130
    button.height = 40

    button = Button(frame, ident="wash_btn", text="Wash")
    button.x = 525
    button.y = 560
    button.width = 130
    button.height = 40

    button = Button(frame, ident="deal_btn", text="Deal")
    button.x = 525
    button.y = 600
    button.width = 130
    button.height = 40

    button = Button(frame, ident="mirror_btn", text="Mirror")
    button.x = 675
    button.y = 520
    button.width = 130
    button.height = 40

    button = Button(frame, ident="show_btn", text="Show")
    button.x = 675
    button.y = 560
    button.width = 130
    button.height = 40

    button = Button(frame, ident="hide_btn", text="Hide")
    button.x = 675
    button.y = 600
    button.width = 130
    button.height = 40

    label = Label(frame, text="Text Input:")
    label.x = 425
    label.y = 650

    text_edit = TextEdit(frame, ident="name_edt", text="(enter here)")
    text_edit.x = 550
    text_edit.y = 650

    # the card table
    table = Table(frame, ident="card_table", deck = deck, hands = hands)
    return frame

class Echo(object):
    def on_echo(self, evt):
        print ("echo:")
        print (evt.text)

    def on_keypress(self, evt):
        print (evt.key)


class Table(Widget):

    def __init__(self, parent=None, deck = None, hands=[], **kwargs):
        super(Table, self).__init__(parent, **kwargs)
        self.x = 0
        self.y = 0
        self.width = 1024
        self.height = 600
        self.color = (160,160,160)
        self.border_color = (255,255,255)
        self.deck = deck
        self.hands = hands


    def render(self, surface):
##        surface.fill(self.color, (self.x+1, self.y+1, self.width-2, self.height-2))
##        pygame.draw.lines(surface,
##                          self.border_color, True,
##                          ((self.x, self.y),
##                           (self.x+self.width, self.y),
##                           (self.x+self.width, self.y+self.height),
##                           (self.x, self.y+self.height)))
        horizontal_adjustment = 85
        for card in self.deck.cards:
            card.render(surface, (horizontal_adjustment,150))
            horizontal_adjustment+=15
        if hands != []:
            for y, hand in enumerate(self.hands):
                for x, card in enumerate(hand.cards):
                    card.render(surface, (x*15+150+y*150,300))


class TestController(GUIController):

    # event handlers

    def on_clicked_from_new_btn(self, evt):
        global deck
        deck.make_new_deck_order()
        self.ev_manager.post_event("gui_redraw")


    def on_clicked_from_save_btn(self, evt):
        print ("Saving has failed. Save has not occurred.")


    def on_clicked_from_load_btn(self, evt):
        print ("Attempting to load from text input.")
        global text_edit
        global deck
        self.load_from_text_input()

    def load_from_text_input(self):
        if text_edit.text.lower() == "eight kings" or "8 kings":
            deck.create_deck_from(EIGHT_KINGS)
        elif text_edit.text.lower() == "si stebbins":
            deck.create_deck_from(SI_STEBBINS)
        elif text_edit.text.lower() == "memorandum":
            deck.create_deck_from(MEMORANDUM)
        elif text_edit.text.lower() == "mnemonica":
            deck.create_deck_from(MNEMONICA)
        elif text_edit.text.lower() == "aronson":
            deck.create_deck_from(ARONSON)
        self.ev_manager.post_event("gui_redraw")

    def on_clicked_from_clear_btn(self, evt):
        print ("Cleared the text input.")
        global text_edit
        text_edit.text = ""
        self.ev_manager.post_event("gui_redraw")

    def on_clicked_from_mirror_btn(self,evt):
        print ("Did the mirror function. It's only useful on NDO.")
        global deck
        deck.mirror()
        self.ev_manager.post_event("gui_redraw")

    def on_clicked_from_faro_btn(self, evt):
        print ("This will execute faro code")
        global deck
        global text_edit
        if text_edit.text != "":
            try:
                faro_count = int(text_edit.text)
                deck.outfaro(faro_count)
            except ValueError:
                deck.outfaro()
        else:
            deck.outfaro()
        self.ev_manager.post_event("gui_redraw")


    def on_clicked_from_antifaro_btn(self, evt):
        print ("This will execute antifaro")
        global deck
        global text_edit
        if text_edit.text != "":
            try:
                antifaro_count = int(text_edit.text)
                deck.antifaro(antifaro_count)
            except ValueError:
                deck.antifaro()
        else:
            deck.antifaro()
        self.ev_manager.post_event("gui_redraw")


    def on_clicked_from_cut_btn(self, evt):
        """Cut the deck. If parameter = None, then cut exact at 26 (half)"""
        global deck
        global text_edit
        if text_edit.text != "":
            try:
                cut_location = int(text_edit.text)
                deck.cut(location=cut_location)
            except ValueError:
                deck.cut()
        else:
            deck.cut()
        self.ev_manager.post_event("gui_redraw")

    def on_clicked_from_riffle_btn(self, evt):
        print ("simulated riffle shuffle button clicked")
        global deck
        deck.riffle()
        self.ev_manager.post_event("gui_redraw")


    def on_clicked_from_wash_btn(self, evt):
        print ("GHSHSHSHSHSERKRK I am a washing machine")
        global deck
        deck.shuffle()
        self.ev_manager.post_event("gui_redraw")


    def on_clicked_from_deal_btn(self, evt):
        global deck
        global hands

        card_count = 5*4
        current_hand = 0
        if len(deck.cards) > card_count:
            while card_count > 0:
                hands[current_hand].add_card(deck.cards.pop(0))
                current_hand+=1
                if current_hand == 4:
                    current_hand = 0
                card_count -= 1
        else:
            print ("Not enough cards left in the deck.")

        self.ev_manager.post_event("gui_redraw")


    def on_clicked_from_show_btn(self, evt):
        global deck
        global hands
        deck.show_all()
        for hand in hands:
            for card in hand.cards:
                card.show()
        self.ev_manager.post_event("gui_redraw")


    def on_clicked_from_hide_btn(self, evt):
        global deck
        global hands
        deck.hide_all()
        for hand in hands:
            for card in hand.cards:
                card.hide()
        self.ev_manager.post_event("gui_redraw")


    def on_clicked_from_any(self, evt):
        print ("generic clicked")


##    def on_keypress(self, evt):
##        key = pygame.key.name(evt.key)
##        pygame.quit()
##        sys.exit()

    ## Prepare the Deck

##    How to make a deck in Si Stebbins
##    deck.make_a_deck_in(CHASED_SUITS)
##    deck.make_si_stebbins()

## Simulate dealing 5 card hands to 4 different players.

##    deck.memorandum()

##    How to make eight kings
##    example_deck = Deck()
##    example_deck.create_deck_from(EIGHT_KINGS)

##    deck_order = deck.return_deckstring()
##    example_deck_order = example_deck.return_deckstring()
##    print deck_order

##    if deck_order == example_deck_order:
##        print "The decks perfectly match!"
##    else:
##        print deck_order
##        print example_deck_order

## PROGRAM MAIN LOOP ##

def run_program():
    global deck, hands

    deck = Deck()
    deck.make_new_deck_order()
##    deck.spit_it_out()

    hands = [Hand() for h in range(4)]

##    deck.memorandum()
##    deck.cards = deck.cards[0:3][::-1]+deck.cards[3:]
##    deck.hide_all()

    pygame.init()

    screen=pygame.display.set_mode((1024,768),HWSURFACE|DOUBLEBUF|RESIZABLE)
    background=pygame.image.load("backgrounds/example.png")#You need an example picture in the same folder as this file!
    screen.blit(pygame.transform.scale(background,(1024,768)),(0,0))

    em = EventManager() # message hub for events
    echo = Echo()
    em.register(echo)

    controller = TestController(em, screen)

    view = create_widgets()
    controller.set_root(view)
    controller.start()

    em.run()

if __name__ == "__main__":
    run_program()


def run_program():
    global deck, hands

    deck = Deck()
    deck.make_new_deck_order()
##    deck.spit_it_out()

    hands = [Hand() for h in range(4)]

##    deck.memorandum()
##    deck.cards = deck.cards[0:3][::-1]+deck.cards[3:]
##    deck.hide_all()

    pygame.init()

    screen=pygame.display.set_mode((1024,768),HWSURFACE|DOUBLEBUF|RESIZABLE)
    background=pygame.image.load("backgrounds/example.png")#You need an example picture in the same folder as this file!
    screen.blit(pygame.transform.scale(background,(1024,768)),(0,0))

    em = EventManager() # message hub for events
    echo = Echo()
    em.register(echo)

    controller = TestController(em, screen)

    view = create_widgets()
    controller.set_root(view)
    controller.start()

    em.run()

if __name__ == "__main__":
    run_program()
