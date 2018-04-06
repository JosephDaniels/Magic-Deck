
## All the Import Boilerplate goes Here.

import random

import pprint

import pygame

import time

import sys

from pygame.locals import *  ## Import stuff we don't need

## Gui Library Imports

import math, glob

from gui import *


## CARD VALUES AND SUITS ##

CARD_VALUES = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]

CARD_VALUE_DICT = {
    "A" : "Ace",
    "2" : "Two",
    "3" : "Three",
    "4" : "Four",
    "5" : "Five",
    "6" : "Six",
    "7" : "Seven",
    "8" : "Eight",
    "9" : "Nine",
    "T": "Ten",
    "J" : "Jack",
    "Q" : "Queen",
    "K" : "King"
    }

CARD_SUIT_DICT = {
    "C" : "Clubs",
    "H" : "Hearts",
    "S" : "Spades",
    "D" : "Diamonds"
    }

## ORDER CONSTANTS

CHASED_SUITS = ["C", "H", "S", "D"]  ## The "Chased Order." NA
SHOCKED_SUITS = ["S", "H", "C", "D"] ## The "Shocked Order." EU
NDO_SUITS = ["H", "C", "D", "S"] ## New Deck Order. Bicycle suit order from out of the box.

## DECK CONSTANTS

MEMORANDUM = "JS7CTHAD4C7H4DAS4H7D4SAHTD7SJCKDTS8CJHACKS5C8H3DQSKH9CQH6C9H2D3C6H5D2S3H8D5SKCJD8STC2C5H6D3S2H9D6SQCQD9S"
EIGHT_KINGS = "8CKH3STD2C7H9S5DQC4HAS6DJC8HKS3DTC2H7S9D5CQH4SAD6CJH8SKD3CTH2S7D9C5HQS4DAC6HJS8DKC3HTS2D7C9H5SQD4CAH6SJD"
SI_STEBBINS = "AC4H7STDKC3H6S9DQC2H5S8DJCAH4S7DTCKH3S6D9CQH2S5D8CJHAS4D7CTHKS3D6C9HQS2D5C8HJSAD4C7HTSKD3C6H9SQD2C5H8SJD"

## Helper Function

flatten = lambda l: [i for s in l for i in s] ## Takes multiple decks and assembles them into one


#
# Globals
#

deck = None
hands = []
text_edit = None


## Our mission is to create a Deck Instance that mimics a real deck.

# We Create a deck instance, it is filled with cards, and it maintains an order.

# We can do permutations on the deck such as faro shuffles, "real" riffle shuffles,

# outfaros (deals) and random shuffles. (wash)

# As Cards are dealt, they are marked as not being "present" in the deck. This is so that cards cannot

# Be dealt again in the same cycle / hand.

# When we are done with the deck we can clear() it.


class Card(object):
    def __init__(self,card_index):
        self.value = card_index[0]
        self.suit = card_index[1]
        self.face = pygame.transform.scale(pygame.image.load("card_images/"+CARD_VALUE_DICT[card_index[0]]+"of"+CARD_SUIT_DICT[card_index[1]]+".png"), (87,122))
        self.back = pygame.transform.scale(pygame.image.load("card_images/RedDotsCardBack.png"), (87,122))
        self.dealt = False
        self.face_up = True

    def deal(self):
        self.dealt = True ## What does this do?

    def show(self):
        self.face_up = True

    def hide(self):
        self.face_up = False

    def render(self, screen, position):
        if self.face_up == True:
            screen.blit(self.face,position)
        else:
            screen.blit(self.back,position)

    def __str__(self):
        return self.value+self.suit

class Deck(object):
    ''' Handles the card objects and contains the deck order.'''
    def __init__(self):
        self.cards = []
        self.make_new_deck_order()


    def add_card(self, card):
        self.cards.append(card)


    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)


    def show_all(self):
        for card in self.cards:
            card.show()

    def hide_all(self):
        for card in self.cards:
            card.hide()


    def make_new_deck_order(self):
        ## Makes a deck in NDO
        self.make_a_deck_in(NDO_SUITS)
        ## Cut the Cards into top and bottom sections
        top_half, bottom_half = self.cut_the(self.cards)
        ## Reverse the bottom half, so we see the ace of spades. AK AK KA KA
        new_deck = top_half + bottom_half[0:13][::-1] + bottom_half[13:26][::-1]
        self.cards = new_deck


    def make_a_deck_in(self,suit_order):
        ## Makes a deck in a specific suit order, AK AK AK AK
        card_indexes = [value+suit for suit in suit_order for value in CARD_VALUES]
        self.construct_from(card_indexes)


    def construct_from(self,card_indexes):
        self.cards = []
        for card_index in card_indexes:
            card = Card(card_index)
            self.add_card(card)

        
    def create_deck_from(self,deck_order):
        self.clear()
        self.construct_from([deck_order[i:i+2] for i in range(0, len(deck_order), 2)])


    def return_deckstring(self):
        deck_order = ""
        for card in self.cards:
            deck_order+=str(card)
        return deck_order


    def mirror(self):
        ## Works on a deck in NDO
        ## Cuts the 13 Clubs cards to the top of the deck
        self.cards = self.cards[13:26] + self.cards[0:13] + self.cards[26:52]


    def print_me(self):
        pretty_deck = []
        for index, card in enumerate(self.cards):
            new_card = list(card)
            expanded_value = CARD_VALUE_DICT[new_card[0]]
            expanded_suit = CARD_SUIT_DICT[new_card[1]]
            pretty_deck.append(expanded_value+" of "+expanded_suit)
        return pretty_deck


    def memorandum(self):
        ## Sets the deck in Memorandum Stack.
        self.clear()
        self.make_new_deck_order()
        self.mirror()
        self.outfaro(4)
        self.cards = self.cards[1:12]+[self.cards[0]]+self.cards[12:]
        self.cards = self.cards[44:]+self.cards[0:44]
        self.cards = self.cards[0:34]+[self.cards[51]]+self.cards[34:51]
        self.cards = self.cards[0:24]+self.cards[34:]+self.cards[24:34]
        self.cards = self.cards[0:24]+[self.cards[27]]+self.cards[24:27]+self.cards[28:]


    def make_si_stebbins(self, suit_order):
        ## Sets the deck in Si Stebbins Order, given a suit order.
        self.clear()
        self.make_a_new_deck_in(suit_order)
        top_half, bottom_half = self.cut_the(self.cards)
        clubs, hearts = self.cut_the(top_half)
        spades, diamonds = self.cut_the(bottom_half)
        clubs, hearts, spades, diamonds = clubs[::-1],hearts[::-1],spades[::-1],diamonds[::-1]
        clubs = [clubs[12]]+clubs[0:12]
        hearts = hearts[9:]+hearts[0:9]
        spades = spades[6:]+spades[0:6]
        diamonds = diamonds[3:]+diamonds[0:3]
        new_deck = []
        for a,b,c,d in zip(clubs,hearts,spades,diamonds):
            new_deck.extend([a,b,c,d])
        self.cards = new_deck


    def clear(self):
        self.cards = []

    def cut(self, location=26):
        top_half, bottom_half = self.cards[0:location], self.cards[location:]
        self.cards = bottom_half+top_half

    def cut_the(self,deck):
        top_half = len(deck)/2
        return deck[:top_half], deck[top_half:]


    def outfaro(self,faro_number=1):
        for shuffles in range(faro_number):
            ## A shuffle that cuts the deck in half and performs an out faro,
            ## This leaves the Ace of spades on bottom and Ace of Clubs on top.
            self.cards = flatten([[x, y] for x, y in zip(*self.cut_the(self.cards))])


    def antifaro(self,antifaro_number=1):
        for shuffles in range(antifaro_number):
            top_half = []
            bottom_half = []
            for i in range(0,len(self.cards),2):
                top_half.append(self.cards[i])
                bottom_half.append(self.cards[i+1])
            self.cards = top_half + bottom_half


    def spit_it_out(self):
        print self.print_me()


    def shuffle(self):
        random.shuffle(self.cards)


    def riffle(self, perfect_cut=False):
        ## It should cut the deck, and simulate an imperfect riffle shuffle.
        ## That means that parts of the deck are left unshuffled and fall in clumps.
        if perfect_cut == False:
            cut_location = 26+random.randint(-5,5)
        else:
            cut_location = 26
        top_half, bottom_half = self.cards[0:cut_location], self.cards[cut_location:]
            
        shuffled_deck = []
        cards_left = True
        alternation_flag = random.randint(0,1)
        while cards_left == True:
            ## Stop if done
            if len(top_half) == 0 or len(bottom_half) == 0:
                if len(top_half) == 0:
                    shuffled_deck.extend(bottom_half)
                if len(bottom_half) == 0:
                    shuffled_deck.extend(top_half)
                cards_left = False
            
            chunk = random.randint(1,4)
            
            if alternation_flag == 0 and chunk <= len(top_half):
                alternation_flag = 1
                for i in range(chunk):
                    shuffled_deck.append(top_half.pop(0))
                    
            if alternation_flag == 1 and chunk <= len(bottom_half):
                alternation_flag = 0
                for x in range(chunk):
                    shuffled_deck.append(bottom_half.pop(0))
                    
        self.cards = shuffled_deck

class Hand(object):
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def show_hand(self):
        for card in self.cards:
            card.show()

    def hide_hand(self):
        for card in self.cards:
            card.hide()


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

    button = Button(frame, ident="mirror_btn", text="Mirror")
    button.x = 225
    button.y = 640
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

    button = Button(frame, ident="next", text="Next")
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

    label = Label(frame, text="Parameter:")
    label.x = 350
    label.y = 650
    
    text_edit = TextEdit(frame, ident="name_edt", text="(numbers only)")
    text_edit.text = "What the?"
    text_edit.x = 500
    text_edit.y = 650

    # the card table
    table = Table(frame, ident="card_table", deck = deck, hands = hands)
    return frame

class Echo(object):
    def on_echo(self, evt):
        print "echo:"
        print evt.text
        
    def on_keypress(self, evt):
        print evt.key


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
            card.render(surface, (horizontal_adjustment,200))
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
        print "Saving has failed. Save has not occurred."


    def on_clicked_from_load_btn(self, evt):
        print "Loading failed."


    def on_clicked_from_mirror_btn(self,evt):
        print "Did the mirror function. It's only useful on NDO."
        global deck
        deck.mirror()
        self.ev_manager.post_event("gui_redraw")

    def on_clicked_from_faro_btn(self, evt):
        print "This will execute faro code"
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
        print "This will execute antifaro"
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
        print "cutting the deck, if parameter = None, then cut exact at 26 (half)"
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
        print "simulated riffle shuffle button clicked"
        global deck
        deck.riffle()
        self.ev_manager.post_event("gui_redraw")


    def on_clicked_from_wash_btn(self, evt):
        print "GHSHSHSHSHSERKRK I am a washing machine"
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
            print "Not enough cards left in the deck."
            
        self.ev_manager.post_event("gui_redraw")


    def on_clicked_from_next_btn(self, evt):
        print "Attempting to go next..."


    def on_clicked_from_show_btn(self, evt):
        global deck
        deck.show_all()
        self.ev_manager.post_event("gui_redraw")


    def on_clicked_from_hide_btn(self, evt):
        global deck
        deck.hide_all()
        self.ev_manager.post_event("gui_redraw")

        
    def on_clicked_from_any(self, evt):
        print "generic clicked"


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


