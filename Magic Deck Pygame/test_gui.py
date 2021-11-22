import sys, time, math, glob

import pygame
from gui import *


# create the view, ie the tree of widgets
def create_widgets():
    
    frame = Frame()
    frame.x = 10
    frame.y = 10
    frame.width = 600
    frame.height = 300
    
    label = Label(frame, text="This is a label")
    label.x = 40
    label.y = 260
    
    button = Button(frame, ident="new_btn", text="New")
    button.x = 40
    button.y = 100
    button.width = 130
    button.height = 40

    button = Button(frame, ident="save_btn", text="Save")
    button.x = 40
    button.y = 140
    button.width = 130
    button.height = 40
    
    button = Button(frame, ident="load_btn", text="Load")
    button.x = 40
    button.y = 180
    button.width = 130
    button.height = 40

    button = Button(frame, ident="faro_btn", text="Faro")
    button.x = 180
    button.y = 100
    button.width = 130
    button.height = 40

    button = Button(frame, ident="antifaro_btn", text="Antifaro")
    button.x = 180
    button.y = 140
    button.width = 130
    button.height = 40

    button = Button(frame, ident="cut_btn", text="Cut")
    button.x = 180
    button.y = 180
    button.width = 130
    button.height = 40

    button = Button(frame, ident="riffle_btn", text="Riffle")
    button.x = 320
    button.y = 100
    button.width = 130
    button.height = 40

    button = Button(frame, ident="wash_btn", text="Wash")
    button.x = 320
    button.y = 140
    button.width = 130
    button.height = 40

    button = Button(frame, ident="deal_btn", text="Deal")
    button.x = 320
    button.y = 180
    button.width = 130
    button.height = 40

    button = Button(frame, ident="next", text="Next")
    button.x = 460
    button.y = 100
    button.width = 130
    button.height = 40

    button = Button(frame, ident="show_btn", text="Show")
    button.x = 460
    button.y = 140
    button.width = 130
    button.height = 40

    button = Button(frame, ident="hide_btn", text="Hide")
    button.x = 460
    button.y = 180
    button.width = 130
    button.height = 40
    
    text_edit = TextEdit(frame, ident="name_edt", text="test")
    text_edit.x = 200
    text_edit.y = 260

    return frame


class Echo(object):
    def on_echo(self, evt):
        print ("echo:")
        print (evt.text)
        
    def on_keypress(self, evt):
        print (evt.key)
        

class TestController(GUIController):
    
    # event handlers

    def on_clicked_from_bonjour_btn(self, evt):
        self.ev_manager.post_event("sendme", target_address = "echo")
        

    def on_clicked_from_allo_btn(self, evt):
        print ("allo")
    
    def on_clicked_from_any(self, evt):
        print ("generic clicke evt")
        
        
def test_gui():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    
    em = EventManager() # message hub for events
    echo = Echo()
    em.register(echo)
    controller = TestController(em, screen)
    
    

    view = create_widgets()
    controller.set_root(view)
    controller.start()
    
    em.run()
    
    pygame.quit()
    

if __name__ == "__main__":
    test_gui()
    
