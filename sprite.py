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
        self.images_rects = []

        count = 0

        # Iterate over files in the specified directory
        for root_dir, cur_dir, files in os.walk(fr"characters/{id}"):
            for file in files:
                # Ensure only image files are processed, this example assumes files are PNG
                if file.endswith('.png') or file.endswith('.jpg'):
                    image_path = os.path.join(root_dir, file)
                    self.image = pg.image.load(image_path).convert_alpha() # .convert_alpha() makes it transperant
                    self.rect = self.image.get_rect() # rect is in a 4 element array
                    self.images.append(self.image)  # Add the loaded image to the list
                    self.images_rects.append(self.rect) # add the rect to the rect list
                    count += 1




    def render(self, image_index, x, y ):
        image = self.images[image_index]
        rect = self.images_rects[image_index]

        rect.topleft = (x + (rect.width/2), y + (rect.height/2)) # set x and y to the middle of the rect
        self.screen.blit(image)


    def rotate(self, image_index, degrees):
        image = self.images[image_index]
    
        # rotate the image
        rotated_image = pg.transform.rotate(image, degrees)
        
        # update it in the list
        self.images[image_index] = rotated_image



    def move_smooth(self,image_index, newX, newY, speed=1):
        movedX = False
        movedY = False
        rect = self.images_rects[image_index]

        if not movedY and not movedX:
            # Horizontal movement
            if abs(newX - rect.x) <= speed:
                rect.x = newX
                movedX = True
            elif newX > rect.x:
                rect.x += speed
    
            elif newX < rect.x:
                rect.x -= speed


            # Vertical movement
            if abs(newY - rect.y) <= speed:
                rect.y = newY
                movedY = True
            elif newY > rect.y:
                rect.y += speed

            elif newY < rect.y:
                rect.y -= speed

            




    def move(self,image_index, newX, newY):
        image = self.images[image_index]
        rect = self.images_rects[image_index]
        rect.x = newX
        rect.y = newY
        return
    
    
    def transform(self, image_index, newWidth, newHeight,):
        pass


    def transform_smooth()
        pass
