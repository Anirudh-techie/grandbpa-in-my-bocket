import random
import math
import pygame

class Particles:
   def __init__(self, x, y,particles):
      self.x = x
      self.y = y
      self.particles = []
      for i in range(particles):
         self.particles.append(Particle(x, y))
   
   def draw(self, screen):
      for particle in self.particles:
         particle.move()
         particle.draw(screen)
         if particle.speed < 2:
            self.particles.remove(particle)
      if len(self.particles) == 0:
         return True
      return False

   def reset(self, x, y,particles):
      self.__init__(x, y,particles)

class Particle:
   def __init__(self, x, y):
      self.x = x
      self.y = y
      # self.speed = random.randint(3, 5)
      self.speed = random.randint(2, 4)

      self.direction = random.randint(0, 360)
      r = random.random()
      # self.color = ((r<0.33)*255, (r>0.33 and r<0.66)*255, (r>0.66)*255)
      self.color = (0,0,200)
      self.radius = random.randint(1, 5)
   
   def move(self):
      self.x += self.speed * math.cos(math.radians(self.direction))
      self.y += self.speed * math.sin(math.radians(self.direction))
      self.speed *= 0.98
   
   def draw(self, screen):
      pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
   