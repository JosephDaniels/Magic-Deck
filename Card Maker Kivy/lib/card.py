from collections import OrderedDict

import pygame

class Card(object):
    ORDERED_VALUES = [
      "A", "2", "3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "K"
    ]

    VALUES = OrderedDict({
        "A": "Ace",
        "2": "Two",
        "3": "Three",
        "4": "Four",
        "5": "Five",
        "6": "Six",
        "7": "Seven",
        "8": "Eight",
        "9": "Nine",
        "0": "Ten",
        "J": "Jack",
        "Q": "Queen",
        "K": "King"
    })

    SUITS = {
        "C": "Clubs",
        "H": "Hearts",
        "S": "Spades",
        "D": "Diamonds"
    }

    def __init__(self, card_index):
        self.face_up = True
        self.value = card_index[0]
        self.suit = card_index[1]

        if self.value == "T":
          self.value = "0"

        if not self.value in Card.VALUES:
            raise ValueError("No value found called:", "value", self.value)
        if not self.suit in Card.SUITS:
            raise ValueError("No suit found called", "suit", self.suit)

    def __repr__(self):
        return self.value + self.suit

    def __str__(self):
        return ("%s of %s" % (Card.VALUES[self.value], Card.SUITS[self.suit]))

    def Flip(self):
        if self.face_up:
            self.face_up = False
        else:
            self.face_up = True

    def hide(self):
        self.face_up = False

    def show(self):
        self.face_up = True

    def filename(self):
        return "{a}{b}.png".format(a=self.value, b=self.suit)

    def full_filename(self):
        return ("%sof%s.png" % (self.VALUES[self.value],self.SUITS[self.suit]))

def start_test():
     card = Card("AH")
     print(repr(card))
     print(str(card))

if __name__ == "__main__":
     start_test()
