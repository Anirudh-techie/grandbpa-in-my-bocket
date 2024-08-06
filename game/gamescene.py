import pygame
class GameScene:
   def __init__(self, screen,difficulty) -> None:
      self.difficulty = difficulty
      self.font =  pygame.font.Font(None, 25)
      self.screen = screen
      self.is_finished_bool = False

      
   def render(self):
      text = self.font.render(f"Difficulty: {self.difficulty}", True, (0,0,0))
      self.screen.blit(text, (160, 540))

   def keydown(self,key):
      print(key)
      if key == 32:
         self.is_finished_bool = True
      pass

   def is_finished(self):
      return self.is_finished_bool