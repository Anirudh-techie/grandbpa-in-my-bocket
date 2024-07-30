import pygame as pg
import os
class Sprite:
    def __init__(self,screen, name, id, position:list, width, height,  rotation=0, animation_state=1):
        self.screen = screen
        self.pos = position
        self.width = width
        self.height = height
        self.rotation = rotation
        self.images = []  # List to store the loaded images

        count = 0
\


        # Iterate over files in the specified directory
        for root_dir, cur_dir, files in os.walk(fr"characters/{id}"):
            for file in files:
                # Ensure only image files are processed, this example assumes files are PNG
                if file.endswith('.png') or file.endswith('.jpg'):
                    image_path = os.path.join(root_dir, file)
                    image = pg.image.load(image_path).convert_alpha()
                    self.images.append(image)  # Add the loaded image to the list




        self.rect = self.image.get_rect()

    def render(self, state=1):
        self.screen.blit()


    def rotate(self):




    def move(self, newX, newY, smooth=True, speed=1):


