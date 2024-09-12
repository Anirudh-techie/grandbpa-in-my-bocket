import pygame
from game.arrow import Arrow
import random
import pygame
from game.particles import Particle, Particles
from game.fireball import Fireball
pygame.mixer.init()

boss_hps = [200, 300, 500, 1000,5000,2000, 3000, 4000, 5000, 6000]
player_hps = [100,125, 125, 200, 2500, 250, 250, 250, 250, 250] 
attack_dmgs = [1, 3, 5, 8, 10, 5, 5, 5, 5, 5]
boss_dmgs = [2, 4, 5, 10, 15, 50, 100, 150, 200, 250]
bpms = [90, 100, 133, 150, 400, 220, 260, 300, 350, 400]

songs=[pygame.mixer.Sound("res/game/songs/small granbpa vibe.mp3"),
       pygame.mixer.Sound("res/game/songs/battle_theme_regular.mp3"),
       pygame.mixer.Sound("res/game/songs/metal_song.mp3"),
       pygame.mixer.Sound("res/game/songs/granbpa vibe.mp3"),
       pygame.mixer.Sound("res/game/songs/grandbpa vibe harder.mp3"),
       ]

deathBgs = [pygame.image.load("res/game/backgrounds/davyloss.jpg"), 
            pygame.image.load("res/game/backgrounds/gamestoreloss.jpg"),
            pygame.image.load("res/game/backgrounds/applewin.jpg"), 
            pygame.image.load("res/game/backgrounds/penicillinloss.JPG"),
            pygame.image.load("res/game/backgrounds/penicillinloss.JPG"),
            ]

winBgs = [pygame.image.load("res/game/backgrounds/davywin.jpg"),
           pygame.image.load("res/game/backgrounds/gamestorewin.jpg"),
           pygame.image.load("res/game/backgrounds/applewin.jpg"), 
           pygame.image.load("res/game/backgrounds/penicillinwin.JPG"),
           pygame.image.load("res/game/backgrounds/penicillinwin.JPG")
           ]

bad_guys = [
   [pygame.image.load("res/game/bad_guy/djNeutral.png"), pygame.image.load("res/game/bad_guy/djBobbing.png"), pygame.image.load("res/game/bad_guy/djHit.png")],
   [pygame.image.load("res/game/bad_guy/ebNeutral.png"), pygame.image.load("res/game/bad_guy/ebBobbing.png"), pygame.image.load("res/game/bad_guy/ebHit.png")],
   [pygame.image.load("res/game/bad_guy/appleNeutral.png"), pygame.image.load("res/game/bad_guy/appleBobbing.png"), pygame.image.load("res/game/bad_guy/appleHit.png")],
   [pygame.image.load("res/game/bad_guy/penicillinNeutral.png"), pygame.image.load("res/game/bad_guy/penicillinBobbing.png"), pygame.image.load("res/game/bad_guy/penicillinHit.png")],
   [pygame.image.load("res/game/bad_guy/penicillinNeutral.png"), pygame.image.load("res/game/bad_guy/penicillinBobbing.png"), pygame.image.load("res/game/bad_guy/penicillinHit.png")],
]

thresholds = [
   50, 50, 50, 50, 50
]
class GameScene:
   def __init__(self, screen,difficulty) -> None:
      
      self.difficulty = difficulty
      self.font =  pygame.font.Font("res/fonts/blackpearl-font/Blackpearl-vPxA.ttf", 17)
      self.streakFont = pygame.font.Font("res/fonts/blackpearl-font/Blackpearl-vPxA.ttf", 35)
      self.winSound = pygame.mixer.Sound("res/soundfx/gameWinSound.mp3")
      self.screen = screen
      self.song_playing = True
      self.death_screen_sprite = pygame.transform.scale(deathBgs[difficulty-1], (self.screen.get_width(), self.screen.get_height()))
      self.win_screen_sprite = pygame.transform.scale(winBgs[difficulty-1], (self.screen.get_width(), self.screen.get_height()))
      self.background_sprite = pygame.transform.scale(pygame.image.load("res/backgrounds/rhythmbackground.png"), (self.screen.get_width(), self.screen.get_height()))
      self.jamuel_width, self.jamuel_height = 260, 380
      self.dancing_jamuel_sprites = [pygame.transform.scale(pygame.image.load("res/game/jamuel/jamuelNeutral.png"), (self.jamuel_width, self.jamuel_height)), pygame.transform.scale(pygame.image.load("res/game/jamuel/jamuelBobbing.png"), (self.jamuel_width, self.jamuel_height)), pygame.transform.scale(pygame.image.load("res/game/jamuel/jamuelDance.png"), (self.jamuel_width, self.jamuel_height))]
      self.jamuel = self.dancing_jamuel_sprites[0]
      self.reset_arrows_y = -40

      self.varToOnlyLoopOnceForWinScreen = True

      self.bad_guy_width, self.bad_guy_height = 600, 500
      self.bad_guy_sprites = [pygame.transform.scale(bad_guys[difficulty-1][0], (self.bad_guy_width, self.bad_guy_height)), pygame.transform.scale(bad_guys[difficulty-1][1], (self.bad_guy_width, self.bad_guy_height)),pygame.transform.scale(bad_guys[difficulty-1][2], (self.bad_guy_width, self.bad_guy_height))]
      self.bad_guy = self.bad_guy_sprites[0]

      self.is_finished_bool = False


      self.anim_state_number = 0
      
      self.songs = songs
   
      self.current_song = self.songs[self.difficulty-1]
      self.bpm = bpms[difficulty-1]

      self.y_perfect = 50

      y_travel = screen.get_height() + 100 - self.y_perfect

      self.num_arrows_in_screen = 8


      self.gap = y_travel/self.num_arrows_in_screen #high iq tactic to fix beat sync issue
      self.beattimer = 0

      self.speed = self.gap / (60/self.bpm)

      self.up_arrows:list[Arrow] = []
      self.left_arrows:list[Arrow] = []
      self.right_arrows:list[Arrow] = []
      self.down_arrows:list[Arrow] = []
      
      
      self.perfect_threshold = thresholds[difficulty- 1]
      self.penalty_threshold = self.perfect_threshold + 30
      
      self.boss_health = boss_hps[difficulty-1]
      self.boss_max_health = self.boss_health
      self.player_health = player_hps[difficulty-1]
      self.player_max_health = self.player_health

      self.attack_dmg = attack_dmgs[difficulty-1]
      self.boss_dmg = boss_dmgs[difficulty-1]

      self.boss_health_bar_width = self.screen.get_width() * 5/12
      self.boss_health_bar_height = 20
      self.boss_health_bar_x = self.screen.get_width()/2
      self.boss_health_bar_y = 20

      self.player_health_bar_width = self.screen.get_width() * 1/6
      self.player_health_bar_height = 20
      self.player_health_bar_x = self.screen.get_width()/2 + 60
      self.player_health_bar_y = 300

      

      
      self.curr_streak = 0
      
      
      self.right_arrow_img = pygame.transform.scale(pygame.image.load("res/game/arrows/arrow.png"), (75,75))
      self.left_arrow_img = pygame.transform.rotate(self.right_arrow_img, 180)
      self.up_arrow_img = pygame.transform.rotate(self.right_arrow_img, 90)
      self.down_arrow_img = pygame.transform.rotate(self.right_arrow_img, 270)

      self.second_arrow_chance = 2
      
      self.arrow_particle_L = Particles(212,87, 0)
      self.arrow_particle_R = Particles(587,87, 0)
      self.arrow_particle_U = Particles(462,87, 0)
      self.arrow_particle_D = Particles(337,87, 0)


      self.fireballs = []
      
      self.is_lost = True
      self.is_won = False

      self.show_perfect = False
   
   def reset(self):
      self.reset_arrows()
      self.curr_streak = 0
      self.player_health = self.player_max_health
      self.boss_health = self.boss_max_health
      self.anim_state_number = 0
      self.song_playing = True
      self.beattimer = 0
      self.is_lost = True

   def render(self,dt):
      self.update()

      if not self.is_lost:
         self.screen.blit(self.death_screen_sprite, (0,0))

         return
      
      if self.is_won:
         self.current_song.stop()
         self.screen.blit(self.win_screen_sprite, (0,0))


      else:
 
         self.screen.blit(self.background_sprite, (0,0))
      
         
         self.screen.blit(self.bad_guy,(self.screen.get_width()*0.65, self.screen.get_height()*0.28))
         self.screen.blit(self.jamuel, (self.screen.get_width()*0.55, self.screen.get_height()*0.35+20))
         #paticles
         self.arrow_particle_L.draw(self.screen)
         self.arrow_particle_R.draw(self.screen)
         self.arrow_particle_U.draw(self.screen)
         self.arrow_particle_D.draw(self.screen)

         self.screen.blit(self.left_arrow_img, (175, self.y_perfect))
         self.screen.blit(self.down_arrow_img, (300, self.y_perfect))
         self.screen.blit(self.up_arrow_img, (425, self.y_perfect))
         self.screen.blit(self.right_arrow_img, (550, self.y_perfect))
         
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

         
         if self.player_health <= 0:
            self.deathScreen()
            return
         if self.boss_health <= 0:   
            self.is_won = True
            

         self.show_stats()    





   def show_stats(self):
      border_bar_overlay_size_increase = 10

      # grey background rect for player bar
      pygame.draw.rect(self.screen, (20, 20, 20), (self.player_health_bar_x - (border_bar_overlay_size_increase/2), self.player_health_bar_y - (border_bar_overlay_size_increase/2), self.player_health_bar_width + border_bar_overlay_size_increase , self.player_health_bar_height + border_bar_overlay_size_increase))
      # grey background rect for boss bar
      pygame.draw.rect(self.screen, (20, 20, 20), (self.boss_health_bar_x - (border_bar_overlay_size_increase/2), self.boss_health_bar_y - (border_bar_overlay_size_increase/2), self.boss_health_bar_width + border_bar_overlay_size_increase , self.boss_health_bar_height + border_bar_overlay_size_increase))
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



      bh = self.font.render(f"{int(self.boss_health)}", True, (0,0,255))
      self.screen.blit(bh, (self.boss_health_bar_x + 5, self.boss_health_bar_y))

      
      ph = self.font.render(f"{int(self.player_health)}", True, (0,0,255))
      self.screen.blit(ph, (self.player_health_bar_x + 5, self.player_health_bar_y))
      

      for ball in self.fireballs:
         if ball.is_finished:
            self.fireballs.remove(ball)

         # ball.render(self.screen)
   def tickbeat(self,dt):
      self.beattimer += dt

      for arrow in self.up_arrows:
         if arrow.y <= self.reset_arrows_y:
            self.up_arrows.remove(arrow)
            self.curr_streak = 0
            self.player_health -= self.boss_dmg
      for arrow in self.down_arrows:
         if arrow.y <= self.reset_arrows_y:
            self.curr_streak = 0
            self.down_arrows.remove(arrow)
            self.player_health -= self.boss_dmg

      for arrow in self.left_arrows:
         if arrow.y <= self.reset_arrows_y:
            self.curr_streak = 0
            self.left_arrows.remove(arrow)
            self.player_health -= self.boss_dmg

      for arrow in self.right_arrows:
         if arrow.y <= self.reset_arrows_y:
            self.curr_streak = 0
            self.right_arrows.remove(arrow)
            self.player_health -= self.boss_dmg

      if self.curr_streak <= 0:
          self.show_perfect = False
      #streak blit
      if self.show_perfect:
            cs = self.streakFont.render(f"HIT! {int(self.curr_streak)}x", True, (0,200,0))
            self.screen.blit(cs, ( 425 - (cs.get_width()/2), 600))

      if self.beattimer >= 30/self.bpm and self.anim_state_number:
         self.anim_state_number = False
         
      if self.beattimer >= 60/self.bpm:
         
         self.anim_state_number = True
         self.beattimer = self.beattimer - 60/self.bpm #higher iq tactic to fix beat sync issue

         rng1 = round(random.random() * 4)
         rng2 = round(random.random() * 4)
         
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
      if not self.is_lost:
         if key == pygame.K_RETURN:
            self.is_lost = True
            self.reset()
         return
      
      elif self.is_won:
         
         if key == pygame.K_RETURN or pygame.K_SPACE:
            self.game_won()

         return
            

      

      elif key == pygame.K_UP or key == pygame.K_w or key == pygame.K_n:
         if len(self.up_arrows) == 0:
            self.player_health -= self.boss_dmg
         else:
            arrow = self.up_arrows.pop(0)
            self.boss_health -= self.validate(arrow)

      elif key == pygame.K_LEFT or key == pygame.K_a or key == pygame.K_z:
         if len(self.left_arrows) == 0:
            self.player_health -= self.boss_dmg
         else:
            arrow = self.left_arrows.pop(0)
            self.boss_health -= self.validate(arrow)

      elif key == pygame.K_RIGHT or key == pygame.K_d or key == pygame.K_m:
         if len(self.right_arrows) == 0:
            self.player_health -= self.boss_dmg
         else:
            arrow = self.right_arrows.pop(0)
            self.boss_health -= self.validate(arrow)

      elif key == pygame.K_DOWN or key == pygame.K_s or key == pygame.K_x:

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
      self.is_lost = False

   def game_won(self):
      self.winSound.stop()
      self.is_finished_bool = True
      


   def update(self):
      
      if not self.is_won:
         
         self.jamuel = self.dancing_jamuel_sprites[self.anim_state_number]
         self.bad_guy = self.bad_guy_sprites[self.anim_state_number]
         if self.song_playing == True:
            self.current_song.play(-1)
            self.song_playing = False

      else:
         
         if self.varToOnlyLoopOnceForWinScreen:
            self.current_song.stop()
            self.winSound.play(1)
            self.varToOnlyLoopOnceForWinScreen = False
         

   def validate(self, arrow):

      y = arrow.y

      diff = abs(y - self.y_perfect)

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
            
         self.show_perfect = True

         self.curr_streak+=1
         dmg = self.attack_dmg

         if self.curr_streak  <= 16:
            dmg += self.curr_streak
         else:
            dmg += 16


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
