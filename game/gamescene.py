import pygame
from game.arrow import Arrow
import random
class GameScene:
   def __init__(self, screen,difficulty) -> None:
      self.difficulty = difficulty
      self.font =  pygame.font.Font(None, 25)
      self.screen = screen
      self.is_finished_bool = False
   

      self.bpm = 30*difficulty
      self.gap = 50
      self.beattimer = 0

      self.speed = self.gap / (1000/self.bpm)

      self.up_arrows:list[Arrow] = []
      self.left_arrows:list[Arrow] = []
      self.right_arrows:list[Arrow] = []
      self.down_arrows:list[Arrow] = []

      self.score = 0
      self.miss_penalty = -5
      self.perfect_score = 10
      self.perfect_threshold = 10
      self.penalty_threshold = 50


   def render(self,dt:int):
      self.tickbeat(dt)
      for arrow in self.up_arrows:
         arrow.render(self.screen)
      for arrow in self.left_arrows:
         arrow.render(self.screen)
      for arrow in self.right_arrows:
         arrow.render(self.screen)
      for arrow in self.down_arrows:
         arrow.render(self.screen)

   def tickbeat(self,dt):
      self.beattimer += dt

      for arrow in self.up_arrows:
         if arrow.y <= 0:
            self.up_arrows.remove(arrow)
            self.score += self.miss_penalty
      for arrow in self.down_arrows:
         if arrow.y <= 0:
            self.down_arrows.remove(arrow)
            self.score += self.miss_penalty

      for arrow in self.left_arrows:
         if arrow.y <= 0:
            self._aleftrrows.remove(arrow)
            self.score += self.miss_penalty

      for arrow in self.right_arrows:
         if arrow.y <= 0:
            self.right_arrows.remove(arrow)
            self.score += self.miss_penalty


      if self.beattimer >= 1000/self.bpm:
         self.beattimer = 0

         if random.random() < 0.2:
            self.up_arrows.append(Arrow(self.speed, 160, "↑"))
         if random.random() < 0.2: 
            self.left_arrows.append(Arrow(self.speed, 240, "←"))
         if random.random() < 0.2:
            self.right_arrows.append(Arrow(self.speed, 320, "→"))
         if random.random() < 0.2:
            self.down_arrows.append(Arrow(self.speed, 400, "↓"))

   

   def keydown(self,key):
      print(key)
      if key == 32:
         self.is_finished_bool = True

      if key == 119:
         for arrow in self.up_arrows:
            
      pass

   def is_finished(self):
      return self.is_finished_bool