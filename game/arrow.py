import pygame as pg
class Arrow:
   def __init__(self,speed, x, id) -> None: # up = 1, left = 2, right = 3, down = 4
      self.speed = speed
      self.y = 650
      self.x = x
      self.rect = {50, 50, x, 650}
      self.right_arrow_img = pg.transform.scale(pg.image.load("res/game/arrows/arrow.png"), (50,50))

      if id == 1:
         self.arrow_img = pg.transform.rotate(self.right_arrow_img, 90)
      elif id == 4:
         self.arrow_img = pg.transform.rotate(self.right_arrow_img, 270)

      elif id == 2:
         self.arrow_img = pg.transform.rotate(self.right_arrow_img, 180)

         
      elif id == 3:
         self.arrow_img = self.right_arrow_img
         


   def render(self, screen):
      screen.blit(self.arrow_img, (self.x, self.y))

   def update(self, deltaTime):
      self.y -= self.speed * deltaTime
      
   