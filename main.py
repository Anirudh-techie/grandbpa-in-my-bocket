# importing necessary modules
import pygame as pg
from scene import Scene
from parsor import get_scene_data

class Game:
    
    def __init__(self):
        pg.init()
        self.screen_width, self.screen_height = (800, 700)
        self.running = True

        new_icon = pg.image.load("res/icon.jpg")
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
               if event.key == pg.K_ESCAPE:
                     self.running = False
               if isinstance(self.scenes[self.current_scene], Scene):
                  if event.key == pg.K_SPACE:  
                     self.scenes[self.current_scene].next_dialogue()
                  elif event.key == pg.K_DOWN:
                     self.scenes[self.current_scene].next_choice()
                  elif event.key == pg.K_UP:
                     self.scenes[self.current_scene].prev_choice()
               else:
                  self.scenes[self.current_scene].keydown(event.key)
            
            if isinstance(self.scenes[self.current_scene], Scene):
               if event.type == pg.MOUSEBUTTONDOWN:
                  self.scenes[self.current_scene].check_mouse_choice(*event.pos)
               if event.type == pg.MOUSEMOTION:
                  self.scenes[self.current_scene].hover_mouse_choice(*event.pos)
        
            

    def render_stuff_loop(self,dt):
         self.screen.fill((255,255,255))
         if self.scenes[self.current_scene].is_finished():
            self.current_scene += 1
            if self.current_scene == len(self.scenes):
                self.running = False
         if isinstance(self.scenes[self.current_scene], Scene):
            self.scenes[self.current_scene].render()
         else: 
            self.scenes[self.current_scene].render(dt)


    def mainLoop(self):

        while self.running:

            dt = self.clock.tick(60)/1000
            self.handle_events()
            self.render_stuff_loop(dt)
            pg.display.update()


if __name__ == "__main__":
    game = Game()
    game.mainLoop()
    pg.quit()

