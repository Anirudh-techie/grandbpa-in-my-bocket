import pygame as pg


class StartScreen: # screen width: 800, screen_height : 700
    def __init__(self, screen, screen_width, screen_height):
        pg.mixer.init()
        self.loading_screen_music = pg.mixer.Sound('res/soundfx/loading_screen_music.ogg')
        self.loading_screen_music.set_volume(0.3)
        self.screen_width, self.screen_height = screen_width, screen_height
        self.screen = screen
        self.background = pg.transform.scale(pg.image.load("res/backgrounds/titlescrenbackground.JPG").convert_alpha(), (screen_width, screen_height))
        self.start_game_button = pg.transform.scale(pg.image.load("res/startScreen/startbuttonHeld.PNG").convert_alpha(), (500, 240))
        self.title = pg.transform.scale(pg.image.load("res/startScreen/logo.PNG"), (screen_width * 2/3 , screen_height/2 ))
        
        
        
        self.button_rect = self.start_game_button.get_rect()
        self.button_rect.x = (self.screen_width/2) - (self.button_rect.width/2)
        self.button_rect.y = (self.screen_height * 8/12)
        self.isStartScreen = True
        self.quitted = False

        # self.title_font = pg.font.Font('res/fonts/blackpearl-font/Blackpearl-vPxA.ttf', 100)
        # self.title_surface = self.title_font.render('Grandbpa In My Bocket', False, (255, 255, 255))
        # self.title_width = self.title_surface.get_width()
        self.loading_screen_music.play(-1)
        
       
    def handle_events(self):
        # self.isStartScreen = False
        self.is_button_pressed = self.button_pressed()
        


        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                self.isStartScreen = False
                self.quitted = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.isStartScreen = False
                    self.quitted = True
                    
            if event.type == pg.KEYDOWN:
                print("key pressed")
            if event.type == pg.MOUSEBUTTONDOWN:
                print("mouse clicked")
                if pg.mouse.get_pressed()[0] and self.is_button_pressed:
                        self.loading_screen_music.stop()
                        print("mouse1 clicked")
                        self.isStartScreen = False
    
    def render(self):
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.start_game_button, self.button_rect)
        self.screen.blit(self.title, ((self.screen_width/2)- self.title.get_width()/2, 40))
    def check_running(self):
        return self.isStartScreen
        
    def button_pressed(self):
        self.mousex, self.mousey = pg.mouse.get_pos()
        self.mouse_rect = pg.Rect(self.mousex, self.mousey, 5, 5)
        if pg.Rect.colliderect(self.mouse_rect, self.button_rect): # check if mouse is over
            self.start_game_button = pg.transform.scale(pg.image.load("res/startScreen/startbutton.PNG").convert_alpha(), (500, 240))
            return True
        else:
            self.start_game_button = pg.transform.scale(pg.image.load("res/startScreen/startbuttonHeld.PNG").convert_alpha(), (500, 240))
            return False
        
    def get_quitted(self):
        return self.quitted

            
    
        