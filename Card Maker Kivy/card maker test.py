from __future__ import division

import time
import sys
import os, os.path
import math
import random

from lib.deck import Deck

import pygame
from pygame.locals import *

from PIL import Image, ImageDraw, ImageFont

def alphamasked(img, green_screen_color):
    """returns an image alpha masked so that pixels with the given
       RGB green_screen_color are made transparent"""
    new_image = img.convert_alpha()
    mask_r, mask_g, mask_b = green_screen_color
    width, height = img.get_size()
    for x in range(width):
        for y in range(height):
            r,g,b,a = new_image.get_at((x,y))
            if  r == mask_r and g == mask_g and b == mask_b:
                new_image.set_at((x,y), (r,g,b,0))
    return new_image


CARD_DIMENSION = (552, 768)
CARD_PADDING = 16

class CardWidget(object):
    Font = ImageFont.truetype('fonts/open-sans/OpenSans-Regular.ttf', 99) # font size

    def __init__(self, card):
        self.card = card
        self.face = None
        self.back = None
        self.face_up = True

    def create_image(self, card_type="bicycle"):
        img_w, img_h = CARD_DIMENSION
        p = CARD_PADDING

        self.image = Image.new("RGBA", (img_w, img_h), color=(255, 255, 255, 255))
        if card_type == "bicycle":
            fg = Image.open("card_images/{a}.png".format(a=self.card.value.upper()))
            sz = fg.size
            self.image.paste(fg, (p, p)) # top left
            self.image.paste(fg.rotate(180), (img_w - sz[0] - p - p, img_h - sz[1] - p - p)) # bottom right
            fg = Image.open("card_images/{b}.png".format(b=self.card.suit.upper()))
            sz2 = fg.size
            self.image.paste(fg, (p, p + p + sz[1])) # top left
            self.image.paste(fg.rotate(180), (img_w - sz[0] - p - p, img_h - sz[1] - sz2[1] - p - p - p)) # bottom right

        elif card_type == "index":
            fg = Image.open("card_images/{a}.png".format(a=self.card.value.upper()))
            sz = fg.size
            sz = (sz[0]*4, sz[1]*4)
            fg = fg.resize(sz, Image.ANTIALIAS)
            self.image.paste(fg, (int(img_w / 2), p))

            fg = Image.open("card_images/{b}.png".format(b=self.card.suit.upper()))
            sz = fg.size
            sz = (sz[0]*4, sz[1]*4)
            fg = fg.resize(sz, Image.ANTIALIAS)
            self.image.paste(fg, (int(img_w / 2), p + sz[0] + p)) # under top middle

        else:
            exception
            return

        self.image.save("image1.png")
        self.face = pygame.image.load("image1.png")

    def show(self):
        self.face_up = True

    def hide(self):
        self.face_up = False

    def render(self, screen, position):
        if self.face_up == True:
            screen.blit(self.face, position)
        else:
            screen.blit(self.back, position)

    def __str__(self):
        return self.card.value+self.card.suit


def main_loop():
    d = Deck()
    d.make_new_deck_order()
    for card in d.cards:
        print str(card)

    pygame.init()
    p = CARD_PADDING
    screen = pygame.display.set_mode((CARD_DIMENSION[0]+p+p, CARD_DIMENSION[1]+p+p)) # in theory

    i = 0
    running = True

    random_card_number = random.randint(0,51)
    card = CardWidget(d.cards[random_card_number])
    card.create_image(card_type="index")

    while running == True:
        screen.fill((0,0,0)) # black

        # draw it
        card.render(screen, (10, 10))

        # more draw coded
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    running = False
                if event.key == pygame.K_RIGHT:

                if event.key == pygame.K_LEFT:
                    card.previous()

            pygame.display.flip()

        time.sleep(1 / 60) # 60 fps
        i+=1

        # quit after 5s
        if i > 60 * 5:
            running = False
            pygame.quit()


if __name__ == "__main__":
    main_loop()
