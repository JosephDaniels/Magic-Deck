from collections import OrderedDict


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
        return self.__str__()

    def __str__(self):
        return "{a}{b}".format(a=self.value, b=self.suit)

    def Flip(self):
        if self.face_up:
            self.face_up = False
        else:
            self.face_up = True

    def Hide(self):
        self.face_up = False

    def Show(self):
        self.face_up = True

    def Filename(self):
        return "{b}{a}.png".format(a=self.value, b=self.suit)
