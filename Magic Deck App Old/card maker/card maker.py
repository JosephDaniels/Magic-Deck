import pygame
from pygame.locals import *
import time
import sys
import os, os.path
import math

##import PIL

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


class Card(object):
    def __init__(self):
        self.index = "AS"
        self.image = None
        self.create_image()
##        self.values = [] ## Will have a list of value images. Ace to King.
##        self.suits = [] ## Will have a list of suit images. Clubs, Hearts, Spades, Diamonds.

    def create_image(self):
        card_image = pygame.transform.scale(pygame.image.load("card_images/BlankCard.png"), (350,488))
        Ace_img = alphamasked(pygame.image.load("card_images/A.png"), (255,255,255))
        Spade_img = alphamasked(pygame.image.load("card_images/spade.png"), (255,255,255))
        self.blank_card_img = card_image
        self.value_img = Ace_img
        self.suit_img = Spade_img
        

    def render(self, screen, location):
        screen.blit(self.blank_card_img,(location))
        screen.blit(self.value_img, (location[0]+15,location[1]+15))
        screen.blit(self.suit_img, (location[0]+20,location[1]+100))
        screen.blit(pygame.transform.rotate(self.value_img, 180), (location[0]+275,location[1]+400))
        screen.blit(pygame.transform.rotate(self.suit_img, 180), (location[0]+280,location[1]+335))
        screen.blit(pygame.transform.scale(self.suit_img, (150,150)), (location[0]+100, location[1]+170))

        
class Background_Manager(object):
    def __init__(self, num_images):
        self.current_image = 0
        self.backgrounds = []
        self.width = 0
        self.height = 0
        self.load_backgrounds(num_images)
        self.set_size()
        self.screen_size = []
        self.cached_background = None # expect imagetype


    def set_size(self):
        print self.backgrounds, self.current_image
        self.width, self.height = self.backgrounds[self.current_image].get_width(), self.backgrounds[self.current_image].get_height()
        self.area = (self.height * self.width)
        self.aspectRatio = (self.width/float(self.height))

        
    def find_height(self,width):
        return int(width/float(self.aspectRatio))


    def find_width(self,height):
        return int(height*float(self.aspectRatio))
        

    def get_current_image(self):
        return self.backgrounds[self.current_image]


    def next_img(self):
        if self.current_image == len(self.backgrounds)-1:
            self.current_image = 0
        else:
            self.current_image+=1
        self.set_size()
        self.resize()

        
    def previous_img(self):
        if self.current_image == 0:
            self.current_image = len(self.backgrounds)-1
        else:
            self.current_image-=1
        self.set_size()
        self.resize()


    def load_cards(self):
        card = pygame.image.load("card_images/BlankCard.png")
        print "failed to load cards."
    
    def load_backgrounds(self,num_images):
        for i in range(0,num_images):
            try:
                image = pygame.image.load("gallery/example" + str(i) + ".jpg")
                self.backgrounds.append(image)
            except:
                try:
                    image = pygame.image.load("gallery/example" + str(i) + ".png")
                    self.backgrounds.append(image)
                    print "example" + str(i) + ".png"
                except:
                    print "Finished."


    def get_center(self, image):
        return image.get_width()/2,image.get_height()/2
        print image.get_width()/2,image.get_height()/2

    def resize(self, x, y):
        self.width = x
        self.height = y
        self.cached_background = pygame.transform.scale(self.backgrounds[self.current_image],(self.width,self.height))
        

    def render(self, screen, location=(0,0)):
        screen.blit(self.cached_background, location)

def main_program():
    
    #Startup
    
##    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
##    infoObject = pygame.display.Info()
##    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h),HWSURFACE|DOUBLEBUF|RESIZABLE)
    screen = pygame.display.set_mode((1080,720),HWSURFACE|DOUBLEBUF|RESIZABLE)
    running = True
    location = (425,150)
    card = Card()
    size = (0,0)

    DIR = 'gallery/'
    num_backgrounds = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    bg_manager = Background_Manager(num_backgrounds)
    print num_backgrounds
    background = None

##    bg_manager.resize(infoObject.current_w, infoObject.current_h)
    bg_manager.resize(bg_manager.get_current_image().get_width(), bg_manager.get_current_image().get_height())
    bg_manager.render(screen)

    center = bg_manager.get_center(bg_manager.get_current_image())
    print center
    
    #Main Loop
    while running == True:
        for event in pygame.event.get():
            background = bg_manager.get_current_image()
            bg_manager.screen_size = screen.get_size()
            if event.type==QUIT: pygame.display.quit()
            
            
            elif event.type==VIDEORESIZE:
                bg_manager.screen_size = event.dict['size']
                bg_manager.resize(bg_manager.screen_size[0],bg_manager.screen_size[1])
##                if bg_control.screen_size[0] > bg_control.height:
##                    width = bg_control.find_width(bg_control.screen_size[1])
##                elif bg_control.screen_size[1] > bg_control.width:
##                    height = bg_control.find_height(bg_control.screen_size[0])
    
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RIGHT:
                    bg_manager.next_img()
                if event.key == pygame.K_LEFT:
                    bg_manager.previous_img()

                    
        bg_manager.render(screen)
        card.render(screen,center)
        pygame.display.flip()
        time.sleep(0.033)

if __name__ == "__main__":
    main_program()
