import pygame
from game.arrow import Arrow
import random
import pygame
class GameScene:
   def __init__(self, screen,difficulty) -> None:
      self.difficulty = difficulty
      self.font =  pygame.font.Font(None, 25)
      self.screen = screen
      self.is_finished_bool = False
   

      self.bpm = 60*difficulty
      self.gap = 100
      self.beattimer = 0

      self.speed = self.gap / (60/self.bpm)

      self.up_arrows:list[Arrow] = []
      self.left_arrows:list[Arrow] = []
      self.right_arrows:list[Arrow] = []
      self.down_arrows:list[Arrow] = []

      self.score = 0
      self.miss_penalty = -5
      self.perfect_score = 10
      self.perfect_threshold = 10
      self.penalty_threshold = 50
      
      
      self.right_arrow_img = pygame.transform.scale(pygame.image.load("res/game/arrows/arrow.png").convert(), (50,50))
      self.left_arrow_img = pygame.transform.rotate(self.right_arrow_img, 180)
      self.up_arrow_img = pygame.transform.rotate(self.right_arrow_img, 90)
      self.down_arrow_img = pygame.transform.rotate(self.right_arrow_img, 270)
      
      # self.up_arrow_img = pygame.transform.scale(pygame.image.load("res/game/arrows/up_arrow.png").convert(), (50,50))
      # self.down_arrow_img = pygame.transform.scale(pygame.image.load("res/game/arrows/down_arrow.png").convert(), (50,50))
      # self.left_arrow_img = pygame.transform.scale(pygame.image.load("res/game/arrows/left_arrow.png").convert(), (50,50))
      

   


   def render(self,dt):
      
      self.screen.blit(self.left_arrow_img, (200, 50))
      self.screen.blit(self.down_arrow_img, (300, 50))
      self.screen.blit(self.up_arrow_img, (400, 50))
      self.screen.blit(self.right_arrow_img, (500, 50))
      
      self.tickbeat(dt)
      for arrow in self.up_arrows:
         arrow.update(dt)
         arrow.render(self.screen)
      for arrow in self.left_arrows:
         arrow.update(dt)
         arrow.render(self.screen)
      for arrow in self.right_arrows:
         arrow.update(dt)
         arrow.render(self.screen)
      for arrow in self.down_arrows:
         arrow.update(dt)
         arrow.render(self.screen)


      self.show_score()



   def show_score(self):
      
      score_text = self.font.render(f"Score: {int(self.score)}", True, (0,0,0))
      self.screen.blit(score_text, (10,10))

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
            self.left_arrows.remove(arrow)
            self.score += self.miss_penalty

      for arrow in self.right_arrows:
         if arrow.y <= 0:
            self.right_arrows.remove(arrow)
            self.score += self.miss_penalty


      if self.beattimer >= 60/self.bpm:
         self.beattimer = 0
         print("spawning")
         if random.random() < 0.2:
            self.up_arrows.append(Arrow(self.speed, 400, 1))
         if random.random() < 0.2: 
            self.left_arrows.append(Arrow(self.speed, 200, 2))
         if random.random() < 0.2:
            self.right_arrows.append(Arrow(self.speed, 500, 3))
         if random.random() < 0.2:
            self.down_arrows.append(Arrow(self.speed, 300, 4))

   

   def keydown(self,key):
      print(key)

      
      if key == pygame.K_SPACE:
         self.is_finished_bool = True

      elif key == pygame.K_UP or key == pygame.K_w:
         if len(self.up_arrows) == 0:
            self.score += self.miss_penalty
         else:
            arrow = self.up_arrows.pop(0)
            self.score += self.validate(arrow)

      elif key == pygame.K_LEFT or key == pygame.K_a:
         if len(self.left_arrows) == 0:
            self.score += self.miss_penalty
         else:
            arrow = self.left_arrows.pop(0)
            self.score += self.validate(arrow)

      elif key == pygame.K_RIGHT or key == pygame.K_d:
         if len(self.right_arrows) == 0:
            self.score += self.miss_penalty
         else:
            arrow = self.right_arrows.pop(0)
            self.score += self.validate(arrow)

      elif key == pygame.K_DOWN or key == pygame.K_s:
         if len(self.down_arrows) == 0:
            self.score += self.miss_penalty
         else:
            arrow = self.down_arrows.pop(0)
            self.score += self.validate(arrow)
                  
   def validate(self, arrow):
      y_perfect = 50
      y = arrow.y

      diff = abs(y - y_perfect)
      if diff < self.perfect_threshold:
         return self.perfect_score
      if diff < self.penalty_threshold:
         return (1 - ((diff - self.perfect_threshold) / (self.penalty_threshold - self.perfect_threshold))) * self.perfect_score
      else:
         return self.miss_penalty


   def is_finished(self):
      return self.is_finished_bool