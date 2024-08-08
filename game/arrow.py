import pygame as pg
class Arrow:
   def __init__(self,speed, x, id) -> None: # up = 1, left = 2, right = 3, down = 4
      self.speed = speed
      self.y = 650
      self.x = x
      self.rect == {50, 50, x, 650}

      if id == 1:
         self.arrow_image = pg.image.load("res/game/arrows/up_arrow.png")
      elif id == 2:
         self.arrow_image = pg.image.load("res/game/arrows/down_arrow.png")
      elif id == 3:
         self.arrow_image = pg.image.load("res/game/arrows/left_arrow.png")
      elif id == 4:

         self.arrow_image = pg.image.load("res/game/arrows/right_arrow.png")


   def render(self, screen):
      screen.blit(self.arrow_image, self.rect)

   def update(self, deltaTime):
      self.y += self.speed * deltaTime
      
   