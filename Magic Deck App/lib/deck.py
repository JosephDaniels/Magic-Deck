from collections import OrderedDict

from card import Card

import random

# Helper Function
flatten = lambda l: [i for s in l for i in s] ## Takes multiple decks and assembles them into one

ORDERS = OrderedDict({
    "New Deck Order": "AH2H3H4H5H6H7H8H9H0HJHQHKHAC2C3C4C5C6C7C8C9C0CJCQCKCKDQDJD0D9D8D7D6D5D4D3D2DADKSQSJS0S9S8S7S6S5S4S3S2SAS",
    "Mirror": "AC2C3C4C5C6C7C8C9C0CJCQCKCAH2H3H4H5H6H7H8H9H0HJHQHKHKDQDJD0D9D8D7D6D5D4D3D2DADKSQSJS0S9S8S7S6S5S4S3S2SAS",
    "Memorandum": "JS7CTHAD4C7H4DAS4H7D4SAHTD7SJCKDTS8CJHACKS5C8H3DQSKH9CQH6C9H2D3C6H5D2S3H8D5SKCJD8STC2C5H6D3S2H9D6SQCQD9S",
    "Si Stebbins": "AC4H7STDKC3H6S9DQC2H5S8DJCAH4S7DTCKH3S6D9CQH2S5D8CJHAS4D7CTHKS3D6C9HQS2D5C8HJSAD4C7HTSKD3C6H9SQD2C5H8SJD",
    "Eight Kings": "8CKH3STD2C7H9S5DQC4HAS6DJC8HKS3DTC2H7S9D5CQH4SAD6CJH8SKD3CTH2S7D9C5HQS4DAC6HJS8DKC3HTS2D7C9H5SQD4CAH6SJD",
    "Mnemonica": "4C2H7D3C4H6DAS5H9S2SQH3DQC8H6S5S9HKC2DJH3S8S6HTC5DKD2C3H8D5CKSJD8CTSKHJC7STHAD4S7S4DAC9CJSQD7CQSTD6CAH9D",
    "Aronson": "JSKC5C2H9SAS3H6C8DACTS5H2DKD7D8C3SAD7S5SQDAH8S3D7HQH5D7C4HKH4DTDJCJHTCJD4STH6H3C2S9HKS6S4C8H9CQS6DQC2C9D",
    "My Personal Stack": "4H7C9DQS3C6C8DJH2H5C7DTSAH4C6D9SKH3D5D8SQH2C4D7SJCAC3S6STHKC2D5S9HQCAD4S8HJDKD3H7HTCQD2S6H9CJSAS5H8CTDKS"
})

""" The "Chased Order." NA """
CHASED_SUITS = ["C", "H", "S", "D"]

""" The "Shocked Order." EU """
SHOCKED_SUITS = ["S", "H", "C", "D"]

""" New Deck Order. Bicycle suit order from out of the box. """
NDO_SUITS = ["H", "C", "D", "S"]


class Deck(object):
    """
    Handles the card objects and contains the deck order.
    """
    def __init__(self):
        """
        Makes a deck in NDO
        """
        self.create_deck_from(ORDERS["New Deck Order"])

        # self.make_a_deck_in(NDO_SUITS)
        # # Cut the Cards into top and bottom sections
        # top_half, bottom_half = self.cut_the(self.cards)
        # # Reverse the bottom half, so we see the ace of spades. AK AK KA KA
        # new_deck = top_half + bottom_half[0:13][::-1] + bottom_half[13:26][::-1]
        # self.cards = new_deck

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

    def make_a_deck_in(self, suit_order):
        """
        Makes a deck in a specific suit order, AK AK AK AK
        Ascending Suits Only
        """
        self.construct_from([value+suit for suit in suit_order for value in Card.ORDERED_VALUES])

    def create_deck_from(self, deck_order):
        self.construct_from([deck_order[i:i+2] for i in range(0, len(deck_order), 2)])

    def construct_from(self, card_indexes):
        self.clear()
        for card_index in card_indexes:
            card = Card(card_index)
            self.add_card(card)

    def return_deckstring(self):
        deck_order = ""
        for card in self.cards:
            deck_order += str(card)
        return deck_order

    def validate_deck(self):
        pass

    # def memorandum(self):
    #     """
    #     Sets the deck in Memorandum Stack.
    #     """
    #     self.clear()
    #     self.make_new_deck_order()
    #     self.mirror()
    #     self.outfaro(4)
    #     self.cards = self.cards[1:12]+[self.cards[0]]+self.cards[12:]
    #     self.cards = self.cards[44:]+self.cards[0:44]
    #     self.cards = self.cards[0:34]+[self.cards[51]]+self.cards[34:51]
    #     self.cards = self.cards[0:24]+self.cards[34:]+self.cards[24:34]
    #     self.cards = self.cards[0:24]+[self.cards[27]] + \
    #         self.cards[24:27]+self.cards[28:]
    #
    # def make_si_stebbins(self, suit_order):
    #     """
    #     Sets the deck in Si Stebbins Order, given a suit order.
    #     """
    #     self.clear()
    #     self.make_a_new_deck_in(suit_order)
    #     top_half, bottom_half = self.cut_the(self.cards)
    #     clubs, hearts = self.cut_the(top_half)
    #     spades, diamonds = self.cut_the(bottom_half)
    #     clubs, hearts = clubs[::-1], hearts[::-1],
    #     spades, diamonds = spades[::-1], diamonds[::-1]
    #     clubs = [clubs[12]]+clubs[0:12]
    #     hearts = hearts[9:]+hearts[0:9]
    #     spades = spades[6:]+spades[0:6]
    #     diamonds = diamonds[3:]+diamonds[0:3]
    #     new_deck = []
    #     for a, b, c, d in zip(clubs, hearts, spades, diamonds):
    #         new_deck.extend([a, b, c, d])
    #     self.cards = new_deck

    def clear(self):
        self.cards = []

    def cut(self, location=26):
        top_half, bottom_half = self.cards[0:location], self.cards[location:]
        self.cards = bottom_half+top_half

    def cut_the(self, deck):
        top_half = len(deck)/2
        return deck[:top_half], deck[top_half:]

    def outfaro(self, faro_number=1):
        for shuffles in range(faro_number):
            """
            A shuffle that cuts the deck in half and performs an out faro,
            This leaves the Ace of spades on bottom and Ace of Clubs on top.
            """
            z = self.cut_the(self.cards)
            self.cards = flatten([[x, y] for x, y in zip(*z)])

    def infaro(self, faro_number=1):
        for shuffles in range(faro_number):
            """
            A shuffle that cuts the deck in half and performs an out faro,
            This leaves the Ace of spades on bottom and Ace of Clubs on top.
            """
            z = self.cut_the(self.cards)
            self.cards = flatten([[y, x] for x, y in zip(*z)])

    def antifaro(self, antifaro_number=1):
        for shuffles in range(antifaro_number):
            top_half = []
            bottom_half = []
            for i in range(0, len(self.cards), 2):
                top_half.append(self.cards[i])
                bottom_half.append(self.cards[i+1])
            self.cards = top_half + bottom_half

    def shuffle(self):
        random.shuffle(self.cards)

    def riffle(self, perfect_cut=True):
        """
        It should cut the deck, and simulate an imperfect riffle shuffle.
        That means that parts of the deck are left unshuffled and fall in clumps.

        This should be weighted so that you usually go card by card. (1 by 1)
        """
        if perfect_cut == False:
            cut_location = 26+random.randint(-5, 5)
        elif perfect_cut == True:
            cut_location = 26
        top_half, bottom_half = self.cards[0:
                                           cut_location], self.cards[cut_location:]

        shuffled_deck = []
        cards_left = True
        alternation_flag = random.randint(0, 1)
        while cards_left == True:
            # Stop if done
            if len(top_half) == 0 or len(bottom_half) == 0:
                if len(top_half) == 0:
                    shuffled_deck.extend(bottom_half)
                if len(bottom_half) == 0:
                    shuffled_deck.extend(top_half)
                cards_left = False
                break

            chunk = random.randint(1, 4)

            if alternation_flag == 0 and chunk <= len(top_half):
                alternation_flag = 1
                for i in range(chunk):
                    shuffled_deck.append(top_half.pop(0))

            if alternation_flag == 1 and chunk <= len(bottom_half):
                alternation_flag = 0
                for x in range(chunk):
                    shuffled_deck.append(bottom_half.pop(0))

        self.cards = shuffled_deck
