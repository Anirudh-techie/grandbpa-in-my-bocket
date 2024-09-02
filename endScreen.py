import pygame as pg


class StartScreen: # screen width: 800, screen_height : 700
    def __init__(self, screen, screen_width, screen_height):
        pg.mixer.init()
        self.screen_width, self.screen_height = screen_width, screen_height
        self.screen = screen

        
    
        self.isEndScreen = True
        self.quitted = False

        
       
    def handle_events(self):


        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                self.isEndScreen = False
                self.quitted = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.isStartScreen = False
                    self.quitted = True

    
    def render(self):
        pass
    def check_running(self):
        return self.isEndScreen

    def get_quitted(self):
        return self.quitted

            
    