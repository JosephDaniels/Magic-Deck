def run_program():
    global deck, hands

    deck = Deck()
    deck.make_new_deck_order()
##    deck.spit_it_out()

    hands = [Hand() for h in range(4)]

##    deck.memorandum()
##    deck.cards = deck.cards[0:3][::-1]+deck.cards[3:]
##    deck.hide_all()

    pygame.init()

    screen=pygame.display.set_mode((1024,768),HWSURFACE|DOUBLEBUF|RESIZABLE)
    background=pygame.image.load("backgrounds/example.png")#You need an example picture in the same folder as this file!
    screen.blit(pygame.transform.scale(background,(1024,768)),(0,0))

    em = EventManager() # message hub for events
    echo = Echo()
    em.register(echo)

    controller = TestController(em, screen)

    view = create_widgets()
    controller.set_root(view)
    controller.start()

    em.run()

if __name__ == "__main__":
    run_program()
