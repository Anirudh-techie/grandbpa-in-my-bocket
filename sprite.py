import pygame as pg
import os
from utils import lerp
class Sprite:
    def __init__(self,screen, name, id, width=160, height=90):
        self.screen = screen
        self.current_state = 1
        self.visibility = False
        self.x = 0
        self.y = 0

        self.images = []  # List to store the loaded images
        self.width, self.height = width, height
        self.rect = pg.rect.Rect(self.width, self.height, self.x, self.y)
        

        # Iterate over files in the specified directory
        for root_dir, cur_dir, files in os.walk(fr"res/characters/{id}"):
            for file in files:
                # Ensure only image files are processed, this example assumes files are PNG
                if file.endswith('.png') or file.endswith('.jpg'):
                    image_path = os.path.join(root_dir, file)
                    self.image = pg.image.load(image_path).convert_alpha() # .convert_alpha() makes it transperant
                    self.images.append(self.image)  # Add the loaded image to the list

        self.image = self.images[0] 





    def render(self):

        if self.visibility == True:
            if self.x != 0 and self.y != 0:
                self.rect.topleft = (self.x + (self.rect.width/2), self.y + (self.rect.height/2)) # set x and y to the middle of the rect
            self.screen.blit(self.image, self.rect)
        else:
            return


    def set_state(self, state):
        self.image = self.images[state - 1]
    
    def set_visibility(self, visibility:bool):
        self.visibility = visibility



    def move_smooth(self, newX, newY, speed=1):
         self.x = lerp(self.x, newX, speed/10)
         self.y = lerp(self.y, newY, speed/10)

            




    def move(self, newX, newY):

        self.x = newX
        self.y = newY

    
    
    def transform(selfnewWidth, newHeight,):
        pass


    def transform_smooth():
        pass
