# importing necessary modules
import pygame as pg
from parser import get_scene_data

class Game:
    
    def __init__(self):
        print("INITN")

        pg.init()
        self.screen_width, self.screen_height = (800, 700)
        self.running = True

      #   self.bg_image = pg.image.load('res/backgrounds/background_test.jpg')
        new_icon = pg.image.load("res/icon.jpg")
      #   self.bg_image = pg.transform.scale(self.bg_image, (self.width, self.height))
        pg.display.set_icon(new_icon)

        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))

        self.scenes = get_scene_data(self.screen)
        self.current_scene = 0

        self.clock = pg.time.Clock() 
        pg.display.set_caption("Grandbpa in My Bocket")

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
               if event.key == pg.K_SPACE:  
                  self.scenes[self.current_scene].next_dialogue()
               elif event.key == pg.K_DOWN:
                  self.scenes[self.current_scene].next_choice()
               elif event.key == pg.K_UP:
                  self.scenes[self.current_scene].prev_choice()

            if event.type == pg.MOUSEBUTTONDOWN:
                self.scenes[self.current_scene].check_mouse_choice(*event.pos)
            if event.type == pg.MOUSEMOTION:
                self.scenes[self.current_scene].hover_mouse_choice(*event.pos)
                     

    def render_stuff_loop(self):
         self.screen.fill((255,255,255))
         self.scenes[self.current_scene].render()
      #   self.screen.blit(self.bg_image, (0, 0))


    def mainLoop(self):

        while self.running:

            self.handle_events()
            self.render_stuff_loop()
            pg.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.mainLoop()
    pg.quit()

