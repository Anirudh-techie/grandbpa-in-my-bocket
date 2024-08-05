import pygame as pg
import os
class Sprite:
    def __init__(self,screen, name, id, width=160, height=90):
        self.screen = screen
        self.current_state = 1

        self.images = []  # List to store the loaded images
        self.width, self.height = width, height
        self.rect = pg.rect.Rect(self.width, self.height, 0, 0)
        

        # Iterate over files in the specified directory
        for root_dir, cur_dir, files in os.walk(fr"res/characters/{id}"):
            for file in files:
                # Ensure only image files are processed, this example assumes files are PNG
                if file.endswith('.png') or file.endswith('.jpg'):
                    image_path = os.path.join(root_dir, file)
                    self.image = pg.image.load(image_path).convert_alpha() # .convert_alpha() makes it transperant
                    self.images.append(self.image)  # Add the loaded image to the list

        self.image = self.images[0] 





    def render(self,x, y):


        self.rect.topleft = (x + (self.rect.width/2), y + (self.rect.height/2)) # set x and y to the middle of the rect
        self.screen.blit(self.image, self.rect)


    def set_state(self, state):
        self.image = self.images[state - 1]



    def move_smooth(self,image_index, newX, newY, speed=1):
        movedX = False
        movedY = False
        rect = self.images_rects[image_index]

        if not movedY and not movedX:
            # Horizontal movement
            if abs(newX - self.rect.x) <= speed:
                self.rect.x = newX
                movedX = True
            elif newX > self.rect.x:
                self.rect.x += speed
    
            elif newX < self.rect.x:
                self.rect.x -= speed


            # Vertical movement
            if abs(newY - self.rect.y) <= speed:
                self.rect.y = newY
                movedY = True
            elif newY > self.rect.y:
                self.rect.y += speed

            elif newY < self.rect.y:
                self.rect.y -= speed

            




    def move(self, newX, newY):

        self.rect.x = newX
        self.rect.y = newY

    
    
    def transform(selfnewWidth, newHeight,):
        pass


    def transform_smooth():
        pass
