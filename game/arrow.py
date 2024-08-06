import pygame
class Arrow:
   def __init__(self,speed,x, icon:str) -> None:
      self.speed = speed
      self.x = x
      self.y = 600
      self.icon = icon
      self.font = pygame.font.Font(None, 40)

   def render(self, screen):
      text = self.font.render(self.icon, True, (0,0,0))
      screen.blit(text, (self.x, self.y))

   def validate(self,y:int):
      return abs(y - self.y)
   
   