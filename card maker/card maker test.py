import pygame
from pygame.locals import *
import time
import sys
import os, os.path
import math

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

NDO_SUITS = ["H", "C", "D", "S"] ## New Deck Order. Bicycle suit order from out of the box.


class Card(object):
    def __init__(self, card_index):
        self.value = card_index[0]
        self.suit = card_index[1]
        self.face = None
        self.back = None
        self.face_up = True
        self.create_image()

    def create_image(self):
        card_image = pygame.Surface()
        blank_img = pygame.transform.scale(pygame.image.load("card_images/BlankCard.png"), (350,488))
        ace_img = alphamasked(pygame.image.load("card_images/A.png"), (255,255,255))
        spade_img = alphamasked(pygame.image.load("card_images/spade.png"), (255,255,255))
        self.blank_card_img = card_image
        self.value_img = Ace_img
        self.suit_img = Spade_img
##        screen.blit(self.blank_card_img,(location))
##        screen.blit(self.value_img, (location[0]+15,location[1]+15))
##        screen.blit(self.suit_img, (location[0]+20,location[1]+100))
##        screen.blit(pygame.transform.rotate(self.value_img, 180), (location[0]+275,location[1]+400))
##        screen.blit(pygame.transform.rotate(self.suit_img, 180), (location[0]+280,location[1]+335))
##        screen.blit(pygame.transform.scale(self.suit_img, (150,150)), (location[0]+100, location[1]+170))



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


    def cut_the(self,deck):
        top_half = len(deck)/2
        return deck[:top_half], deck[top_half:]


def main_loop():
    d = Deck()
    d.make_new_deck_order()
    for card in d.cards:
        print str(card)
    pygame.init()
    screen = pygame.display.set_mode((1080,720))
    running = True
    while running = True:
        

if __name__ == "__main__":
    main_loop()
