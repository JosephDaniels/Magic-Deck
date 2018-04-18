class Hand(object):
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def show(self):
        for card in self.cards:
            card.show()

    def hide(self):
        for card in self.cards:
            card.hide()
