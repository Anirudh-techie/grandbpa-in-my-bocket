import pygame
from utils import lerp
import random
class Fireball:
   def __init__(self, position, targetPosition, size, intensity) -> None:
         self.position = position
         self.targetPosition = targetPosition
         self.size = size
         self.intensity = intensity
         self.particles = []
         self.speed = 0.5
         self.is_finished = False

         for i in range(size*10):
               self.particles.append(FireParticle(2, intensity, size))


   def render(self, screen):
      if self.intensity > 1:
            self.intensity = 0

      self.intensity+=0.001

      self.position = lerp(self.position[0], self.targetPosition[0], self.speed),lerp(self.position[1], self.targetPosition[1], self.speed)
      for particle in self.particles:
          particle.intensity = self.intensity
          particle.render(screen, self.position)

      if self.position == self.targetPosition:
         self.is_finished = True
      
       
class FireParticle:
    def __init__(self, size, intensity, vibrateRadius) -> None:
        self.size = size
        self.intensity = intensity
        self.vibrate = vibrateRadius

    def render(self, screen, pos):
        x = pos[0] + random.gauss(0, self.vibrate)
        y = pos[1] + random.gauss(0, self.vibrate)
        
        x_offset = abs(x - pos[0])
        y_offset = abs(y - pos[1])

       


        dist_from_pos = (x_offset**2 + y_offset**2)**0.5
        max_dist = 2*(2**0.5) * self.vibrate
        color = fire_intensity_color(self.intensity - (1 - abs((max_dist - dist_from_pos)/max_dist)) * 0.3)

        max_alpha = 255
        num_layers = 5

        for i in range(num_layers, 0, -1):
            radius = self.size + i+1
            alpha = max_alpha // (i+1)
            bloom_color = (*color, alpha)

            bloom_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(bloom_surface, bloom_color, (radius, radius), radius)
            screen.blit(bloom_surface, (x - radius, y - radius))

        pygame.draw.circle(screen, color, (x,y), self.size)


def fire_intensity_color(intensity):
    intensity = min(1, max(0, intensity))
    colors = [
    (139, 0, 0),          # Dark Red (600-800°C)
    (255, 69, 0),         # Red-Orange (800-900°C)
    (255, 140, 0),        # Orange (900-1000°C)
    (255, 165, 0),        # Bright Orange (1000-1100°C)
    (173, 216, 230),      # Light Blue (1500-1700°C)
    (255,255,255)
    ]

    
    idx = int(intensity * (len(colors) - 1))
    next_idx = min(idx + 1, len(colors) - 1)
    factor = (intensity * (len(colors) - 1)) - idx
    
    r = int(colors[idx][0] + (colors[next_idx][0] - colors[idx][0]) * factor)
    g = int(colors[idx][1] + (colors[next_idx][1] - colors[idx][1]) * factor)
    b = int(colors[idx][2] + (colors[next_idx][2] - colors[idx][2]) * factor)
    
    return (r, g, b)
