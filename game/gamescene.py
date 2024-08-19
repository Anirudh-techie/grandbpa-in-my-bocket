import pygame
from game.arrow import Arrow
import random
import pygame

boss_hps = [200, 300, 500, 1000,1500,2000]
player_hps = [100,125, 125, 200, 250, 250] 
attack_dmgs = [1,2,2,4,5,5]
boss_dmgs = [2,4,5,10,25]

class GameScene:
   def __init__(self, screen,difficulty) -> None:
      self.difficulty = difficulty
      self.font =  pygame.font.Font(None, 25)
      self.screen = screen
      self.is_finished_bool = False
   

      self.bpm = 30*difficulty
      self.gap = 100
      self.beattimer = 0

      self.speed = self.gap / (60/self.bpm)

      self.up_arrows:list[Arrow] = []
      self.left_arrows:list[Arrow] = []
      self.right_arrows:list[Arrow] = []
      self.down_arrows:list[Arrow] = []

      self.boss_dmg = boss_dmgs[difficulty-1]
      self.perfect_threshold = 10
      self.penalty_threshold = 50
      
      self.boss_health = boss_hps[difficulty-1]
      self.player_health = player_hps[difficulty-1]

      self.attack_dmg = attack_dmgs[difficulty-1]
      self.curr_streak = 0
      
      
      self.right_arrow_img = pygame.transform.scale(pygame.image.load("res/game/arrows/arrow.png").convert(), (50,50))
      self.left_arrow_img = pygame.transform.rotate(self.right_arrow_img, 180)
      self.up_arrow_img = pygame.transform.rotate(self.right_arrow_img, 90)
      self.down_arrow_img = pygame.transform.rotate(self.right_arrow_img, 270)

      self.second_arrow_chance = 5


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


      self.show_health()



   def show_health(self):
      
      health = self.font.render(f"Boss Health: {int(self.boss_health)}\nPlayer Health: {int(self.player_health)}\nCurrent Streak: {int(self.curr_streak)}", True, (0,0,0))
      self.screen.blit(health, (10,10))

   def tickbeat(self,dt):
      self.beattimer += dt

      for arrow in self.up_arrows:
         if arrow.y <= 0:
            self.up_arrows.remove(arrow)
            self.player_health -= self.boss_dmg
      for arrow in self.down_arrows:
         if arrow.y <= 0:
            self.down_arrows.remove(arrow)
            self.player_health -= self.boss_dmg

      for arrow in self.left_arrows:
         if arrow.y <= 0:
            self.left_arrows.remove(arrow)
            self.player_health -= self.boss_dmg

      for arrow in self.right_arrows:
         if arrow.y <= 0:
            self.right_arrows.remove(arrow)
            self.player_health -= self.boss_dmg


      if self.beattimer >= 60/self.bpm:
         self.beattimer = 0

         rng1 = round(random.random() * 5)
         rng2 = round(random.random() * 5)
         
         if rng1 == 1:
            self.up_arrows.append(Arrow(self.speed, 400, 1))
         if rng1 == 2: 
            self.left_arrows.append(Arrow(self.speed, 200, 2))
         if rng1 == 3:
            self.right_arrows.append(Arrow(self.speed, 500, 3))
         if rng1 == 4:
            self.down_arrows.append(Arrow(self.speed, 300, 4))

         if round(random.random() * 100 < self.second_arrow_chance):
            if rng2 == 1:
               self.up_arrows.append(Arrow(self.speed, 400, 1))
            if rng2 == 2: 
               self.left_arrows.append(Arrow(self.speed, 200, 2))
            if rng2 == 3:
               self.right_arrows.append(Arrow(self.speed, 500, 3))
            if rng2 == 4:
               self.down_arrows.append(Arrow(self.speed, 300, 4))

   

   def keydown(self,key):
   
      if key == pygame.K_SPACE:
         self.is_finished_bool = True

      elif key == pygame.K_UP or key == pygame.K_w:
         if len(self.up_arrows) == 0:
            self.player_health -= self.boss_dmg
         else:
            arrow = self.up_arrows.pop(0)
            self.boss_health -= self.validate(arrow)

      elif key == pygame.K_LEFT or key == pygame.K_a:
         if len(self.left_arrows) == 0:
            self.player_health -= self.boss_dmg
         else:
            arrow = self.left_arrows.pop(0)
            self.boss_health -= self.validate(arrow)

      elif key == pygame.K_RIGHT or key == pygame.K_d:
         if len(self.right_arrows) == 0:
            self.player_health -= self.boss_dmg
         else:
            arrow = self.right_arrows.pop(0)
            self.boss_health -= self.validate(arrow)

      elif key == pygame.K_DOWN or key == pygame.K_s:
         if len(self.down_arrows) == 0:
            self.player_health -= self.boss_dmg
         else:
            arrow = self.down_arrows.pop(0)
            self.boss_health -= self.validate(arrow)

      if self.player_health < 0:
         self.game_over(False)
         return
      if self.boss_health < 0:
         self.game_over(True)
   
   def game_over(self,didWin):
      if didWin:
         print("You won!")
         self.is_finished_bool = True
      else:
         print("You lost!")
         self.__init__(self.screen, self.difficulty)
                  
   def validate(self, arrow):
      y_perfect = 50
      y = arrow.y

      diff = abs(y - y_perfect)

      if diff < self.perfect_threshold:
         self.curr_streak+=1
         dmg = self.attack_dmg
         if self.curr_streak > 3 and self.curr_streak < 10:
            dmg += 5
         elif self.curr_streak >= 10:
            dmg += 10
         return dmg
      if diff < self.penalty_threshold:
         self.curr_streak = 0
         return 0
         # return (1 - ((diff - self.perfect_threshold) / (self.penalty_threshold - self.perfect_threshold))) * self.attack_dmg
      else:
         self.curr_streak = 0
         self.player_health -= self.boss_dmg
         return 0
      
      

   def is_finished(self):
      return self.is_finished_bool