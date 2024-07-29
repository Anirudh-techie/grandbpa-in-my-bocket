import pygame
font = pygame.font.Font(None, 25)

class Dialogue:
    def __init__(self, text:str, choices=[], sprite_states={}):
        self.text = text
        self.choices = choices
        self.sprite_states = sprite_states
        pass
    def render(self, screen):
        t = font.render(self.text, True, (0,0,0))
        screen.blit(t, (10, 400))