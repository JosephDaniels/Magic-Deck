
## All the Import Boilerplate goes Here.

import random

import pprint

import pygame

from pygame.locals import *

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

CHASED_SUITS = ["C", "H", "S", "D"]  ## The "Chased Order."
SHOCKED_SUITS = ["S", "H", "C", "D"] ## The "Shocked Order."
NDO_SUITS = ["H", "C", "D", "S"] ## New Deck Order. Bicycle suit order from out of the box.

def cut_the(deck):
    half = len(deck)/2
    return deck[:half], deck[half:]

def make_a_deck(suit_order):
    return [value+suit for suit in suit_order for value in CARD_VALUES]

def make_new_deck():
    top_half, bottom_half = cut_the(make_a_deck(NDO_SUITS))
    ## Reverse the bottom half, so we see the ace of spades.
    return top_half + bottom_half[0:13][::-1] + bottom_half[13:26][::-1]

def make_mirror(deck):
    return deck[13:26] + deck[0:13] + deck[26:52]

flatten = lambda l: [i for s in l for i in s]

def out_faro(deck):
    ## A shuffle that cuts the deck in half and performs an out faro,
    ## This leaves the Ace of spades on bottom and Ace of Clubs on top.
    return flatten([[x, y] for x, y in zip(*cut_the(deck))])

def memorandum():
    ## Returns a deck in Memorandum Stack.
    ## For now, it returns a standard faro 4 deck without the adjustment.
    mirror_deck = (make_mirror(make_new_deck()))
    faro4deck = out_faro(out_faro(out_faro(out_faro(mirror_deck))))
    return faro4deck

def remove_whitespace(prettydeck):
    imagelist = [card.replace(" ","") for card in prettydeck]
    return imagelist

class Card(object):
    def __init__(self,card_index):
        self.value = card_index[0]
        self.suit = card_index[1]
        self.image = pygame.image.load("card_images/"+CARD_VALUE_DICT[card_index[0]]+"of"+CARD_SUIT_DICT[card_index[1]]+".png")

class Deck(object):
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)

    def print_me(self):
        pretty_deck = []
        for index, card in enumerate(self.cards):
            new_card = list(card)
            expanded_value = CARD_VALUE_DICT[new_card[0]]
            expanded_suit = CARD_SUIT_DICT[new_card[1]]
            pretty_deck.append(expanded_value+" of "+expanded_suit)
        return pretty_deck

    def spit_it_out(self):
        print self.print_me()


## PROGRAM MAIN LOOP ##

showtime = True
pygame.init()

if __name__ == "__main__":

    
    
    ## Begin Screen Setup
    screen=pygame.display.set_mode((800,600),HWSURFACE|DOUBLEBUF|RESIZABLE)
    
    background=pygame.image.load("backgrounds/example.png")#You need an example picture in the same folder as this file!
   
    screen.blit(pygame.transform.scale(background,(800,600)),(0,0))

    pygame.display.flip()

    ## Prepare the Deck

    deck = Deck()
  
    for card_index in make_new_deck():
        card = Card(card_index)
        deck.add_card(card)
    
    while showtime == True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print ("""
                    Escape Key Detected. Quitting the App.
                    """)
                    pygame.quit()
                    showtime=False
            elif event.type==QUIT: pygame.display.quit()
            elif event.type==VIDEORESIZE:
                screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                screen.blit(pygame.transform.scale(background,event.dict['size']),(0,0))
            horizontal_adjustment = 0
            for card in deck.cards:
                screen.blit(card.image, (horizontal_adjustment,0))
                horizontal_adjustment += 15
        pygame.display.flip()
    pygame.quit()


