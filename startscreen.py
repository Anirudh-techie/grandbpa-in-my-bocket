import pygame as pg


class StartScreen: # screen width: 800, screen_height : 700
    def __init__(self, screen, screen_width, screen_height):
        self.screen_width, self.screen_height = screen_width, screen_height
        self.screen = screen
        self.background = pg.transform.scale(pg.image.load("res/backgrounds/start_screen.jpg").convert_alpha(), (screen_width, screen_height))
        self.start_game_button = pg.image.load("res/buttons/start_game.png").convert_alpha()
        self.running = True
        
        
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:

                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False

    
    def render(self):
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.start_game_button, (self.screen_width, self.screen_height))
        
        
    def mainLoop(self):
        while self.running:
            self.handle_events()
            self.render
            pg.display.update()
            
        
        