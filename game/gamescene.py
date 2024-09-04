import pygame
from game.arrow import Arrow
import random
import pygame
from game.particles import Particle, Particles
from game.fireball import Fireball
pygame.mixer.init()
# master of puppets bpm is 116
boss_hps = [200, 300, 500, 10,1500,2000, 3000, 4000, 5000, 6000]
player_hps = [100,125, 125, 200, 250, 250, 250, 250, 250, 250] 
attack_dmgs = [1, 2, 2, 4, 5, 5, 5, 5, 5, 5]
boss_dmgs = [2, 4, 5, 10, 25, 50, 100, 150, 200, 250]
bpms = [50, 80, 116, 150, 190, 220, 260, 300, 350, 400]



class GameScene:
   def __init__(self, screen,difficulty) -> None:
      
      self.difficulty = difficulty
      self.font =  pygame.font.Font(None, 25)
      self.screen = screen
      self.song_playing = True
      self.death_screen_sprite = pygame.transform.scale(pygame.image.load("res/game/ui/gameoverBackground.jpg"), (self.screen.get_width(), self.screen.get_height()))
      self.background_sprite = pygame.transform.scale(pygame.image.load("res/backgrounds/rhythmbackground.png"), (self.screen.get_width(), self.screen.get_height()))
      self.jamuel_width, self.jamuel_height = 250, 380
      self.dancing_jamuel_sprites = [pygame.transform.scale(pygame.image.load("res/game/jamuel/normal_dancing_jamuel.png"), (self.jamuel_width, self.jamuel_height)), pygame.transform.scale(pygame.image.load("res/game/jamuel/bobbing_dancing_jamuel.png"), (self.jamuel_width, self.jamuel_height)), pygame.transform.scale(pygame.image.load("res/game/jamuel/dancing_dancing_jamuel.png"), (self.jamuel_width, self.jamuel_height))]
      self.jamuel = self.dancing_jamuel_sprites[0]
      self.bad_guy_width, self.bad_guy_height = 300, 500
      self.bad_guy_sprites = [pygame.transform.scale(pygame.image.load("res/game/bad_guy/bad_guy.png"), (self.bad_guy_width, self.bad_guy_height)), pygame.transform.scale(pygame.image.load("res/game/bad_guy/bad guy 2.png"), (self.bad_guy_width, self.bad_guy_height)),pygame.transform.scale(pygame.image.load("res/game/bad_guy/bad guy 3.png"), (self.bad_guy_width, self.bad_guy_height))]
      self.bad_guy = self.bad_guy_sprites[0]
      self.pauseScreenFont = pygame.font.Font('res/fonts/blackpearl-font/Blackpearl-vPxA.ttf', 100)
      self.death_text = self.pauseScreenFont.render("Press Enter to Retry", True, (255,255,255))
      self.is_finished_bool = False
      # self.difficulty3song = pygame.mixer.Sound("res/game/songs/masterofpuppets.mp3")
      # self.difficulty3song.set_volume(0.1)
      self.dancing_jamuel_animation_timer = 0

      self.anim_state_number = 0
      
      self.songs = ["","",pygame.mixer.Sound("res/game/songs/masterofpuppets.mp3"),pygame.mixer.Sound("res/soundfx/granbpa vibe.mp3")]
      self.current_song = self.songs[self.difficulty-1]
      self.bpm = bpms[difficulty-1]
      #self.bpm = 40*difficulty
      self.gap = 100
      self.beattimer = 0

      self.speed = self.gap / (60/self.bpm)

      self.up_arrows:list[Arrow] = []
      self.left_arrows:list[Arrow] = []
      self.right_arrows:list[Arrow] = []
      self.down_arrows:list[Arrow] = []
      
      
      self.perfect_threshold = 20
      self.penalty_threshold = 50
      
      self.boss_health = 1000
      self.boss_max_health = 1000
      self.player_health = 1000
      self.player_max_health = 1000

      self.attack_dmg = 25
      self.boss_dmg = 25

      self.boss_health_bar_width = self.screen.get_width() * 1/3
      self.boss_health_bar_height = 20
      self.boss_health_bar_x = self.screen.get_width()/2 - 50
      self.boss_health_bar_y = 75

      self.player_health_bar_width = self.screen.get_width() * 1/6
      self.player_health_bar_height = 20
      self.player_health_bar_x = self.screen.get_width()/2 - 50
      self.player_health_bar_y = 135

      

      
      self.curr_streak = 0
      
      
      self.right_arrow_img = pygame.transform.scale(pygame.image.load("res/game/arrows/arrow.png"), (75,75))
      self.left_arrow_img = pygame.transform.rotate(self.right_arrow_img, 180)
      self.up_arrow_img = pygame.transform.rotate(self.right_arrow_img, 90)
      self.down_arrow_img = pygame.transform.rotate(self.right_arrow_img, 270)

      self.second_arrow_chance = 5
      
      self.arrow_particle_L = Particles(212,87, 0)
      self.arrow_particle_R = Particles(587,87, 0)
      self.arrow_particle_U = Particles(462,87, 0)
      self.arrow_particle_D = Particles(337,87, 0)


      self.fireballs = []
      
      self.is_gaming = True


      self.test_beat_sfx = pygame.mixer.Sound("res/soundfx/bubble-sound-43207.mp3")
   
   def reset(self):
      self.reset_arrows()
      self.curr_streak = 0
      self.player_health = self.player_max_health
      self.boss_health = self.boss_max_health
      self.anim_state_number = 0
      self.song_playing = True
      self.beattimer = 0
      self.is_gaming = True

   def render(self,dt):
      if not self.is_gaming:
         self.screen.blit(self.death_screen_sprite, (0,0))
         self.screen.blit(self.death_text, (self.screen.get_width()/2  - self.death_text.get_width()/2, self.screen.get_height() * 3/5))
         return
      self.screen.blit(self.background_sprite, (0,0))
   
      
      self.screen.blit(self.bad_guy,(1050, 300))
      self.screen.blit(self.jamuel, (825, 280))
      #paticles
      self.arrow_particle_L.draw(self.screen)
      self.arrow_particle_R.draw(self.screen)
      self.arrow_particle_U.draw(self.screen)
      self.arrow_particle_D.draw(self.screen)

      self.screen.blit(self.left_arrow_img, (175, 50))
      self.screen.blit(self.down_arrow_img, (300, 50))
      self.screen.blit(self.up_arrow_img, (425, 50))
      self.screen.blit(self.right_arrow_img, (550, 50))
      
      self.tickbeat(dt)
      self.update()

      
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
      if self.player_health <= 0:
         self.deathScreen()
         return
      if self.boss_health <= 0:   
         self.winScreen()
         

      self.show_stats()    





   def show_stats(self):
      
      # boss health bar
      # red bar underlay
      pygame.draw.rect(self.screen, (255,0,0), (self.boss_health_bar_x, self.boss_health_bar_y, self.boss_health_bar_width, self.boss_health_bar_height))
      # find percentage
      boss_health_bar_fill_width = (self.boss_health / self.boss_max_health) * self.boss_health_bar_width
      # green bar overlay
      pygame.draw.rect(self.screen, (0, 255, 0), (self.boss_health_bar_x, self.boss_health_bar_y, boss_health_bar_fill_width, self.boss_health_bar_height))

      # for the player___________________________________________________)_@*)&*@^*(#^)
      # red bar underlay
      pygame.draw.rect(self.screen, (255,0,0), (self.player_health_bar_x, self.player_health_bar_y, self.player_health_bar_width, self.player_health_bar_height))
      # find percentage
      player_health_bar_fill_width = (self.player_health / self.player_max_health) * self.player_health_bar_width
      # green bar overlay
      pygame.draw.rect(self.screen, (0, 255, 0), (self.player_health_bar_x, self.player_health_bar_y, player_health_bar_fill_width, self.player_health_bar_height))


      bh = self.font.render(f"Boss Health: {int(self.boss_health)}", True, (0,0,0))
      self.screen.blit(bh, (self.boss_health_bar_x, self.boss_health_bar_y - 25))

      
      ph = self.font.render(f"Player Health: {int(self.player_health)}", True, (0,0,0))
      self.screen.blit(ph, (self.player_health_bar_x, self.player_health_bar_y - 25))
      cs =self.font.render(f"Current Streak: {int(self.curr_streak)}", True, (0,0,0))
      self.screen.blit(cs, (725, 200))

      for ball in self.fireballs:
         if ball.is_finished:
            self.fireballs.remove(ball)

         # ball.render(self.screen)
   def tickbeat(self,dt):
      self.beattimer += dt

      for arrow in self.up_arrows:
         if arrow.y <= -10:
            self.up_arrows.remove(arrow)
            self.player_health -= self.boss_dmg
      for arrow in self.down_arrows:
         if arrow.y <= -10:
            self.down_arrows.remove(arrow)
            self.player_health -= self.boss_dmg

      for arrow in self.left_arrows:
         if arrow.y <= -10:
            self.left_arrows.remove(arrow)
            self.player_health -= self.boss_dmg

      for arrow in self.right_arrows:
         if arrow.y <= -10:
            self.right_arrows.remove(arrow)
            self.player_health -= self.boss_dmg



      if self.beattimer >= 60/self.bpm:
         
         self.anim_state_number = not self.anim_state_number
         self.beattimer = 0

         rng1 = round(random.random() * 5)
         rng2 = round(random.random() * 5)
         
         if rng1 == 1:
            self.up_arrows.append(Arrow(self.screen,self.speed, 425, 1))
         if rng1 == 2: 
            self.left_arrows.append(Arrow(self.screen, self.speed, 175, 2))
         if rng1 == 3:
            self.right_arrows.append(Arrow(self.screen, self.speed, 550, 3))
         if rng1 == 4:
            self.down_arrows.append(Arrow(self.screen, self.speed, 300, 4))

         if round(random.random() * 100 < self.second_arrow_chance):
            if rng2 == 1:
               self.up_arrows.append(Arrow(self.screen, self.speed, 425, 1))
            if rng2 == 2: 
               self.left_arrows.append(Arrow(self.screen, self.speed, 175, 2))
            if rng2 == 3:
               self.right_arrows.append(Arrow(self.screen, self.speed, 550, 3))
            if rng2 == 4:
               self.down_arrows.append(Arrow(self.screen, self.speed, 300, 4))

   
   def keydown(self,key):
      if not self.is_gaming:
         if key == pygame.K_RETURN:
            self.is_gaming = True
            self.reset()
         return

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

   def reset_arrows(self):
      self.down_arrows = []
      self.up_arrows = []
      self.left_arrows = []
      self.right_arrows = []

   
   def deathScreen(self):
      self.current_song.stop()
      self.is_gaming = False

   def winScreen(self):
      self.current_song.stop()
      self.is_finished_bool = True
      


   def update(self):
      
      if self.dancing_jamuel_animation_timer == 5:
         self.dancing_jamuel_animation_timer = 0
         
      self.dancing_jamuel_animation_timer += 1


      self.jamuel = self.dancing_jamuel_sprites[self.anim_state_number]
      self.bad_guy = self.bad_guy_sprites[self.anim_state_number]
      if self.song_playing == True:
         self.current_song.play(-1)
         self.song_playing = False
      

   def validate(self, arrow):

      y_perfect = 50
      y = arrow.y

      diff = abs(y - y_perfect)

      if diff < self.perfect_threshold:
         self.jamuel = self.dancing_jamuel_sprites[2]
         # perfect score appeared
         if arrow.x == 175:
            self.arrow_particle_L.reset(self.arrow_particle_L.x,self.arrow_particle_L.y, 50)
         elif arrow.x == 550:
            self.arrow_particle_R.reset(self.arrow_particle_R.x,self.arrow_particle_L.y, 50)
         elif arrow.x == 425:
            self.arrow_particle_U.reset(self.arrow_particle_U.x,self.arrow_particle_L.y, 50)
         elif arrow.x == 300:
            self.arrow_particle_D.reset(self.arrow_particle_D.x,self.arrow_particle_L.y, 50)

         self.curr_streak+=1
         dmg = self.attack_dmg
         if self.curr_streak > 3 and self.curr_streak < 10:
            dmg += 5
         elif self.curr_streak >= 10:
            dmg += 10

         # self.fireballs.append(Fireball((800,200),(1000,240), int((dmg/15)*5), 0.6))
         self.anim_state_number = 2
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
