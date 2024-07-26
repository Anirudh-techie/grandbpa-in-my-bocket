# importing necessary modules
import pygame as pg
import scene, text


class Game:

    def __init__(self):
        pg.init()

        self.width, self.height = (800, 700)
        self.running = True

        self.bg_image = pg.image.load('res/backgrounds/background_test.jpg')
        new_icon = pg.image.load("res/icon.jpg")
        self.bg_image = pg.transform.scale(self.bg_image, (self.width, self.height))
        pg.display.set_icon(new_icon)

        self.screen = pg.display.set_mode((self.width, self.height))



        pg.display.set_caption("Grandbpa in My Bocket")

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def render_stuff_loop(self):

        self.screen.blit(self.bg_image, (0, 0))
        pg.display.update()

    def mainLoop(self):

        while self.running:
            self.handle_events()

            self.render_stuff_loop()


if __name__ == "__main__":
    game = Game()
    game.mainLoop()
    pg.quit()

