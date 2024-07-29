import pygame as pg
class Sprite:
    def __init__(self,screen, name, id, position:list, width, height,  rotation=0, animation_state=1)
        self.screen = screen
        folder = chara
        self.pos = position
        self.width = width
        self.height = height
        self.rotation = rotation

        self.image = pg.image.load(f"characters/{id}").convert_alpha()
        self.rect = self.image.get_rect()

    def render(self):
        self.screen.blit()


    def rotate(self):




    def move(self, newX, newY, smooth=True, speed=1):


