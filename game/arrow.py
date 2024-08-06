import pygame as pg
class Arrow:
   def __init__(self,speed) -> None:
      self.speed = speed
      self.up_x 
      self.down_x
      self.right_x
      self.left_x

      self.up_arrow = pg.image.load("res/game/arrows/up_arrow.png")
      self.down_arrow = pg.image.load("res/game/arrows/down_arrow.png")
      self.left_arrow = pg.image.load("res/game/arrows/left_arrow.png")
      self.right_arrow = pg.image.load("res/game/arrows/right_arrow.png")
      left_rect = pg.rect.Rect()

   def render(self, screen):
      text = self.font.render(self.icon, True, (0,0,0))
      screen.blit(text, (self.x, self.y))

   def validate(self,y:int):
      return abs(y - self.y)
   
   