
## All the Import Boilerplate goes Here.

import random

import pprint

import pygame

import time

import sys

from pygame.locals import *  ## Import stuff we don't need

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
        self.new_deck_order()


    def add_card(self, card):
        self.cards.append(card)


    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)


    def new_deck_order(self):
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
        self.new_deck_order()
        self.mirror()
        self.out_faro(4)
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


    def cut_the(self,deck):
        top_half = len(deck)/2
        return deck[:top_half], deck[top_half:]


    def out_faro(self,faro_number=1):
        for shuffles in range(faro_number):
            ## A shuffle that cuts the deck in half and performs an out faro,
            ## This leaves the Ace of spades on bottom and Ace of Clubs on top.
            self.cards = flatten([[x, y] for x, y in zip(*self.cut_the(self.cards))])


    def anti_faro(self,antifaro_number=1):
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


    def simulated_riffle(self, perfect_cut=False):
        ## It should cut the deck, and simulate an imperfect riffle shuffle.
        ## That means that parts of the deck are left unshuffled and fall in clumps.
        if perfect_cut == False:
            cut_location = 26+random.randint(-5,5)
        else:
            cut_location = 26
        top_half, bottom_half = self.cards[0:cut_location], self.cards[cut_location:]
            
        shuffled_deck = []
        cards_left = True
        alternation_flag = 0
        while cards_left == True:
            ## Stop if done
            if len(top_half) == 0 or len(bottom_half) == 0:
                shuffled_deck.extend(top_half)
                shuffled_deck.extend(bottom_half)
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


## PROGRAM MAIN LOOP ##

showtime = True
pygame.init()

if __name__ == "__main__":
    ## Begin Screen Setup
    screen=pygame.display.set_mode((1024,768),HWSURFACE|DOUBLEBUF|RESIZABLE)
    
    background=pygame.image.load("backgrounds/example.png")#You need an example picture in the same folder as this file!
   
    screen.blit(pygame.transform.scale(background,(1024,768)),(0,0))

    pygame.display.flip()

    ## Prepare the Deck

##    How to make a deck in Si Stebbins
##    deck.make_a_deck_in(CHASED_SUITS)
##    deck.make_si_stebbins()

    deck = Deck()
    deck.memorandum()
    deck.cards = deck.cards[0:3][::-1]+deck.cards[3:]

    hands = [Hand() for h in range(4)]
    card_count = 5*4
    current_hand = 0
    while card_count > 0:
        hands[current_hand].add_card(deck.cards.pop(0))
        current_hand+=1
        if current_hand == 4:
            current_hand = 0
        card_count -= 1

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

    while showtime == True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print ("""
                    Escape Key Detected. Quitting the App.
                    """)
                    pygame.quit()
                    sys.exit()
            elif event.type==QUIT: pygame.display.quit()
            elif event.type==VIDEORESIZE:
                screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                screen.blit(pygame.transform.scale(background,event.dict['size']),(0,0))
            horizontal_adjustment = 85
            for card in deck.cards:
                card.face_up = False
            for card in deck.cards:
                card.render(screen,(horizontal_adjustment,200))
                horizontal_adjustment+=15
            for y, hand in enumerate(hands):
                for x, card in enumerate(hand.cards):
                    card.render(screen,(x*15+150+y*150,300))
##            horizontal_adjustment = 85
##            for card in example_deck.cards:
##                screen.blit(card.face, (horizontal_adjustment,400))
##                horizontal_adjustment+=15
        pygame.display.flip()
        time.sleep(0.03) #Frame limiter at 30 milliseconds
    pygame.quit()


