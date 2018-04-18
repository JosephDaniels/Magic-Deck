# for easier development, run this from a shell rather than from idle

import sys, time
import weakref
import pygame
import logging



#
# some useful utilites
#

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




    
# base class
class Event(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.method_name = "on_"+name
        self.event_target = None
        self.__dict__.update(kwargs)
        
    def __str__(self):
        return "<"+self.name+">"

    # a helper method
    def clone_attribs_from(self, pe):
        """copy the attributes from a pygame event"""
        attribs = ["gain", "state", "unicode", "key", "mod", "pos", "rel", "button", "size", "w", "h"]
        for k in attribs:
            if hasattr(pe, k):
                self.__dict__[k] = pe.__dict__.get(k)
            



class EventManager(object):
    """handles the passing of event and messages to various objects

    The model used for this system is the publisher/subscriber pattern.
    The EventManager acts like a hub where Event messages can be published.
    Then the manager will check for listeners of 
    
    Any object can publish an event by getting a reference
    to the EventManager and .post("event name", **other_values).

    Listener objects register themselves with the manage via
    the .register(listener) method. On registration, tbe manager will
    inspect the listener for methods with this signature:

        .on_<event_name>(evt)

    Then, when an event is posted to the manager, events of that name are
    appropriately routed to the correct listener method.
    

    Routing:
    ========
        TODO...

    
    """
    
    def __init__(self):
        self.listeners = weakref.WeakKeyDictionary()
        self.event_queue = []
        self.is_running = True
        self.tick_time = 0.033
        self.debug = True
        self.register(self) # in order to listen for quit events

    def register(self, listener):
        self.listeners[listener] = 1

    def unregister(self, listener):
        del self.listeners[listener]

    def post(self, event):
        self.event_queue.append(event)

    def post_event(self, name, **kwargs):
        self.event_queue.append(Event(name, **kwargs))
        
    def on_Quit(self, evt):
        pygame.quit()
        sys.exit()
        

    def run(self):
        while self.is_running:
            # copy the event queue to process...
            curr_events = self.event_queue
            # and reset it for events for the next cycle
            self.event_queue = []
            # retrieve all current pygame events and process into gui events
            for pg_event in pygame.event.get():
                new_event = Event(pygame.event.event_name(pg_event.type))
                new_event.clone_attribs_from(pg_event)
                curr_events.append(new_event)

            # dispatch the events to the relevant listeners
            for event in curr_events:

                if self.debug:
                    ##TODO-use the logging module
                    if event.name != "tick":
                        pass
                        print event
                        
                if event.event_target in self.listeners: # specifically targeted events
                    method = getattr(event.event_target, event.method_name, None)
                    if method != None:
                        method(event)
                else: # no target, so spam all listeners
                    refs = [weakref.ref(obj) for obj in self.listeners]
                    # to copy the weakrefs because the list of listeners may change
                    # during iteration
                    for ref in refs:
                        listener = ref()
                        method = getattr(listener, event.method_name, None)
                        if method != None:
                            method(event)
                       
            time.sleep(self.tick_time)
            self.post_event("tick")

           
        
class Widget(object):
    """base class for all widgets

        
    """
    def __init__(self, parent=None, **kwargs):
        self.ident = kwargs.get("ident", None)
        self.parent = parent
        if parent != None:
            parent.children.append(self)
        self.children = []
        self.rect = pygame.Rect(0,0,0,0)
        self.hover_in = False
        self.padding = 5
        self.ev_manager = None
    

    def render(self, surface):
        raise NotImplementedError


    # property getters/setters
    
    def _get_x(self):
        return self.rect.left

    def _set_x(self, x):
        self.rect.left = x
        
    def _get_y(self):
        return self.rect.top
    
    def _set_y(self, y):
        self.rect.top = y

    def _get_height(self):
        return self.rect.height
    
    def _set_height(self, height):
        self.rect.height = height
        

    def _get_width(self):
        return self.rect.width
    
    def _set_width(self, width):
        self.rect.width = width
      
    def get_padded_size(self):
        return self.width+2*self.padding, self.height+2*self.padding

    def redraw(self):
        self.ev_manager.post_event("gui_redraw")


    def announce(self, msg, **kwargs):
        if self.ident:
            self.ev_manager.post_event(msg+"_from_"+self.ident, **kwargs)
        else:
            self.ev_manager.post_event(msg, **kwargs)
    
    
    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)
    height = property(_get_height, _set_height)
    width = property(_get_width, _set_width)
    

    # helper methods used by  GUIController
    
    def attach(self, controller):
        # helper method to attach a widget and all its children to a controller
        controller.add(self)
        for child in self.children:
            child.attach(controller)
            

    def find_leaf_at(self, x, y):
        # used for finding the widget to set the keyboard focus
        focused = self
        if self.children:
            for child in self.children:
                if child.rect.collidepoint(x,y):
                    focused = child.find_leaf_at(x,y)
        return focused


    
class Button(Widget):
    """
    Announces these events:
        "clicked_from_<ident>" when a button is clicked
        
    """
    def __init__(self, parent=None, text="", **kwargs):
        super(Button, self).__init__(parent, **kwargs)
        self.text = text
        self.x = 0
        self.y = 0
        self.width = 60
        self.height = 30
        self.font_size = 30
        font_name = pygame.font.get_default_font()
        self.font = pygame.font.SysFont(font_name, self.font_size)
        self.font_color = (228,228,228)
        self.face_color = (192,192,192)
        self.shadow_color = (96,96,96)
        self.highlight_color = (255,255,255)
        self.clicked = False
        self.text_padding = 5
        self._set_text(text)
        

    def _render_unclicked(self, surface):
        rendered_text = self.font.render(self.text, True, self.font_color)
        surface.fill(self.shadow_color,
                     (self.x+2, self.y+2, self.width-2, self.height-2))
        surface.fill(self.face_color,
                     (self.x, self.y, self.width-2, self.height-2))
        #center the text on the button face
        text_size = rendered_text.get_size()
        text_width, text_height = text_size
        x_pos = self.x + self.width/2 - text_width/2
        y_pos = self.y + self.height/2 - text_height/2
        surface.blit(rendered_text,  (x_pos, y_pos))

    def _set_text(self, text):
        self.text = text
        w, h = self.font.size(self.text)
        self.width, self.height = w+2*self.text_padding, h+2*self.text_padding
       

    def _render_clicked(self, surface):
        rendered_text = self.font.render(self.text, True, self.font_color)
        surface.fill(self.shadow_color,
                     (self.x, self.y, self.width, self.height))
        surface.fill(self.face_color,
                     (self.x+1, self.y+1, self.width-2, self.height-2))
        #center the text on the button face
        text_size = rendered_text.get_size()
        text_width, text_height = text_size
        x_pos = self.x + self.width/2 - text_width/2
        y_pos = self.y + self.height/2 - text_height/2
        surface.blit(rendered_text,  (x_pos+1, y_pos+1))
               

    def render(self, surface):
        if self.clicked:
            self._render_clicked(surface)
        else:
            self._render_unclicked(surface)
            
    def on_click(self, evt):
        if evt.event_target == self:
            self.announce("clicked")
        

    def on_hover_in(self, evt):
        if evt.event_target == self:
            self.font_color = (255,255,255)
            self.redraw()
        

    def on_hover_out(self, evt):
        if evt.event_target == self:
            self.font_color = (228,228,228)
            self.clicked = False
            self.redraw()

    def on_mouse_down(self, evt):
        if evt.event_target == self:
            self.clicked = True
            self.redraw()

    def on_mouse_up(self, evt):
        if self.clicked == True:
            self.clicked = False
            self.ev_manager.post_event("click", event_target=self)
            self.ev_manager.post_event("gui_redraw")
            
        


class CheckBox(Widget):
    """
    Announces these events:
        checked_on_from_<ident>
        checked_off_from_<ident>
        
    """
    def __init__(self, parent=None):
        super(CheckBox, self).__init__(parent)
        self.x = 0
        self.y = 0
        self.width = 20
        self.height = 20
        self.checked = False
        self.border_color = (128,128,128)
        self.face_color = (255,255,255)
        self.check_color = (0,0,0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def render_checked(self, surface):
        self.render_unchecked(surface)
        pygame.draw.line(surface, self.check_color,
                         (self.x+2, self.y+2),
                         (self.x+self.width-2, self.y+self.height-2))
        pygame.draw.line(surface, self.check_color,
                         (self.x+2, self.y+self.height-2),
                         (self.x+self.width-2, self.y+2))
        
    def render_unchecked(self, surface):
        surface.fill(self.border_color, (self.x, self.y, self.width, self.height))
        surface.fill(self.face_color, (self.x+2, self.y+2,self.width-4, self.height-4))

    def render(self, surface):
        if self.checked:
            self.render_checked(surface)
        else:
            self.render_unchecked(surface)

    def toggle(self):
        self.checked = not self.checked

    def on_mouse_down(self, evt):
        self.toggle()
        self.redraw()
        


class Label(Widget):
    def __init__(self, parent=None, text=""):
        super(Label, self).__init__(parent)
        self.text = text
        self.color = (255,255,255)
        self.x = 0
        self.y = 0
        self.font_size = 30
        font_name = pygame.font.get_default_font()
        self.font = pygame.font.SysFont(font_name, self.font_size)
        self.font_color = (255,255,255)
        print self.font
        print self.text
        self.width, self.height = self.font.size(self.text)
        self.text_y_offset = 3
        self.text_x_offset = 0

    def render(self, surface):
        rendered_text = self.font.render(self.text, True, self.font_color)
        surface.blit(rendered_text, (self.x+self.text_x_offset,
                                     self.y+self.text_y_offset))

    def _set_text(self, text):
        self.text = text
        self.width, self.height = self.font.size(self.text)
        self.redraw()
        

class TextEdit(Widget):
    """
    Announces these events:
        text_changed_from_<ident>
    """
    def __init__(self, parent=None, text="", **kwargs):
        super(TextEdit, self).__init__(parent, **kwargs)
        self.text = text
        self.x = 0
        self.y = 0

        self.width = 200
        self.height = 30
        self.font_size = 30
        self.max_chars = 128

        self.cursor_delay = 10
        self.cursor_countdown = self.cursor_delay
        self.cursor_on = False

        self.repeat_delay = 30
        self.repeat_rate = 10
        self.repeat_countdown = self.repeat_delay
        
        font_name = pygame.font.get_default_font()
        self.font = pygame.font.SysFont(font_name, self.font_size)
        self.color = (0,0,0)
        self.insert_pos = 0
        self.insert_mode = False
        self.text_x_offset = 3
        self.text_y_offset = 3

        self.is_focused = False
        self.focus_color = 255, 0,0

        self.is_editable = True

        self.background = 255,255,255
        

    def render(self, surface):
        text = self.text
        if self.cursor_on:
            text += "_"
        pygame.draw.rect(surface, self.background,
                         (self.x, self.y, self.width, self.height))
        if self.is_focused:
            pygame.draw.rect(surface, self.focus_color,
                             (self.x, self.y, self.width, self.height), 1)
        rendered_text = self.font.render(text, True, self.color)
        surface.set_clip(self.rect)
        surface.blit(rendered_text, (self.x+self.text_x_offset,
                                     self.y+self.text_y_offset))
        surface.set_clip(None)


    def on_focus_in(self, evt):
        if self.is_editable:
            self.is_focused = True
            self.cursor_on = True
            self.redraw()

    def on_focus_out(self, evt):
        if self.is_editable:
            self.is_focused = False
            self.cursor_on = False
            self.redraw()

        
    def on_keypress(self, evt):
        if self.is_editable:
            key = pygame.key.name(evt.key)
            if key == "backspace":
                if len(self.text) > 0:
                    self.text = self.text[:-1]
            elif key == "space":
                self.text += " "
            else:
                if len(key)==1:
                    self.text += key
            self.redraw()

    def on_tick(self, evt):
        if self.is_focused:
            self.cursor_countdown -= 1
            if self.cursor_countdown == 0:
                self.cursor_on = not self.cursor_on
                self.cursor_countdown = self.cursor_delay
                self.redraw()


class Grid(Widget):
    def __init__(self, parent = None, **kwargs):
        super(Grid, self).__init__(parent, **kwargs)
        self.children = []
        self.color = (160,160,160)
        self.border_color = (255,255,255)
        self.x = 0
        self.y = 0
        self.width = 200
        self.height = 200
        self.rows = []
        self.rows.append([])
        self.curr_row = self.rows[0]
        # for tracking the cell heights and widths
        self.heights = [0]
        self.widths = [0]

    def _increase_rows_to(self, n):
        while len(self.rows)<=n:
            self.rows.append([None])
        while len(self.heights)<=n:
            self.heights.append(0)
            

    def _increase_columns_to(self, n):
        while len(self.curr_row) <= n:
            self.curr_row.append(None)
        while len(self.widths) <= n:
            self.widths.append(0)
            

    def add(self, widget, column = -1, row = -1):
        """add the widget to the grid, if the column or row are
        unspecified, the widget is appended to the end of the last row"""

        width, height = widget.get_padded_size()
        
        if row == -1 or column == -1:
            row = len(self.rows)
            column = len(self.rows[row]) + 1
            
        if row >= len(self.rows):
            self._increase_rows_to(row)
        self.curr_row = self.rows[row]

        if column >= len(self.curr_row):
            self._increase_columns_to(column)

        self.children.append(widget)
        self.rows[row][column] = widget

        if self.heights[row] < height:
            self.heights[row] = height
        if self.widths[column] < width:
            self.widths[column] = width

        widget.parent = self


    def pack(self):
        """takes the children and positions them into the parent"""
        y = self.y
        for  row, height in zip(self.rows, self.heights):
            x = self.x
            for widget, width in zip(row, self.widths):
                if widget:
                    widget.x = x+widget.padding
                    widget.y = y+widget.padding
                x += width
            y += height
        self.width = sum(self.widths)
        self.height = sum(self.heights)
        

    def render(self, surface):
        surface.fill(self.color, (self.x+1, self.y+1, self.width-2, self.height-2))
        pygame.draw.lines(surface,
                          self.border_color, True,
                          ((self.x, self.y),
                           (self.x+self.width, self.y),
                           (self.x+self.width, self.y+self.height),
                           (self.x, self.y+self.height)))
        for child in self.children:
            child.render(surface)
                                                  

                      


class Frame(Widget):
    def __init__(self, parent=None, **kwargs):
        super(Frame, self).__init__(parent, **kwargs)
        self.x = 0
        self.y = 0
        self.width = 100
        self.height = 100
        self.color = (160,160,160)
        self.border_color = (255,255,255)
        

    def render(self, surface):
        surface.fill(self.color, (self.x+1, self.y+1, self.width-2, self.height-2))
        pygame.draw.lines(surface,
                          self.border_color, True,
                          ((self.x, self.y),
                           (self.x+self.width, self.y),
                           (self.x+self.width, self.y+self.height),
                           (self.x, self.y+self.height)))



class Spinner(Widget):
    def __init__(self, parent=None, **kwargs):
        super(Spinner, self).__init__(parent, **kwargs)
        self.x = 0
        self.y = 0
        self.width = 100
        self.height = 50
        self.color = 0,0,0
        self.border_color = (255,255,255)

        self.min_value = 0
        self.max_value = 100
        self.curr_value = 50
        self.increment = 5
        

    def _render_arrows(self):
        pass
        
    def render(self, surface):
        pygame.draw.lines(surface,
                          self.border_color, True,
                          ((self.x, self.y),
                           (self.x+self.width, self.y),
                           (self.x+self.width, self.y+self.height),
                           (self.x, self.y+self.height)))




class GUIController(object):
    """Base for gui apps. The GUI Controller interacts with a set of widgets
    and the screen where the widgets are rendered. To use

    a) Derive a new class from GUIController
    b) Create your widget tree
    c) Set the root widget
    d) Create listener methods[*] to handle events from the widgets
    e) create an instance of your new class, and .start() that instance

    [*] a design goal was to separate the view from the controller as
    much as possible. In other gui libraries, callbacks are usually set in
    the create widgets section of the program. I feel this ties the
    widget creation too close to the process of creating the controller. 
    
    """

    def __init__(self, ev_manager, surface):
        self.ev_manager = ev_manager
        ev_manager.register(self)
        self.surface = surface
        self.widgets = []
        self.focused_widget = None
        self.need_redraw = False
        self.is_running = False
        self.root = None # the root widget
        

    def start(self):
        self.focused_widget = self.root
        self.is_running = True
        self.redraw() # issue a redraw event to kick everything off


    def add(self, widget):
        widget.ev_manager = self.ev_manager
        self.ev_manager.register(widget)
        self.widgets.append(widget)


    def set_root(self, root):
        # walk a widget tree and add to the controller
        def walk(node, action):
            action(node)
            for ch in node.children:
                walk(ch, action)
            
        walk(root, self.add)
        self.root = root


    def redraw(self):
        for w in self.widgets:
            w.render(self.surface)
        pygame.display.flip()


    # event handlers to translate and direct pygame events
    # to the focused widget
    def on_MouseButtonDown(self, evt):
        x, y = evt.pos
        for widget in self.widgets:
            if widget.rect.collidepoint(x,y):
                self.ev_manager.post_event("mouse_down", event_target=widget)
        has_focus= self.root.find_leaf_at(x,y)
        if has_focus != self.focused_widget:
            self.ev_manager.post_event("focus_out", event_target = self.focused_widget)
            self.ev_manager.post_event("focus_in", event_target = has_focus)
            self.focused_widget = has_focus
            

    def on_MouseButtonUp(self, evt):
        for widget in self.widgets:
            self.ev_manager.post_event("mouse_up", event_target=widget)

                
    def on_MouseMotion(self, evt):
        x,y = evt.pos
        for widget in self.widgets:
            if widget.rect.collidepoint(x,y):
                if  widget.hover_in == False:
                    widget.hover_in = True
                    self.ev_manager.post_event("hover_in", event_target=widget)
            else:
                if widget.hover_in == True:
                    widget.hover_in = False
                    self.ev_manager.post_event("hover_out", event_target=widget)


    def on_KeyDown(self, evt):
        if self.focused_widget:
            self.ev_manager.post_event("keypress",
                                       event_target = self.focused_widget,
                                       key=evt.key)


    def on_KeyUp(self, evt):
        pass

    # events specific to the GUIController
    
    def on_gui_redraw(self, evt):
        print "redraw"
        self.redraw()

    def on_quit(self, evt):
        pass



 
        


   
            
            
                
