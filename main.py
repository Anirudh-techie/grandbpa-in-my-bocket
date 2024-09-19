# importing necessary modules
import pygame as pg
from scene import Scene
from parsor import get_scene_data
from startscreen import StartScreen

class Game:
    
    def __init__(self):
        # Initialize Pygame and its mixer for sound
        pg.init()
        pg.mixer.init()
        display_info = pg.display.Info()
        print(f"Display resolution: {display_info.current_w} x {display_info.current_h}")
        print(pg.display.list_modes())

        # Flag to keep track of the game running state
        self.running = True

        # Load and set the game icon
        new_icon = pg.image.load("res/icon.jpg")
        pg.display.set_icon(new_icon)

        # Set up the display mode to fullscreen and get screen dimensions
        # self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        # self.screen = pg.display.set_mode((1920, 1080))
        self.screen_width, self.screen_height = self.screen.get_size()
        
        # Retrieve scene data for the game
        self.scenes = get_scene_data(self.screen, self.screen_width, self.screen_height)
        self.current_scene = 0  # Index of the current scene

        # Initialize the clock for frame rate control
        self.clock = pg.time.Clock() 
        pg.display.set_caption("Grandbpa in My Bocket")  # Set the window caption
        
        # Initialize the start screen
        self.startScreen = StartScreen(self.screen, self.screen_width, self.screen_height)
        self.isStartScreen = True  # Flag to indicate if the start screen is active
        
        
    def handle_events(self):
        # Check if the start screen has been quit
        if self.startScreen.get_quitted():
            self.running = False

        if self.isStartScreen:
            # Handle events for the start screen
            self.startScreen.handle_events()
        else:
            # Handle game events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                # if event.type == pg.MOUSEBUTTONDOWN:
                #     if pg.mouse.get_pressed()[0]:
                #         self.scenes[self.current_scene].next_dialogue()


                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False

                    if isinstance(self.scenes[self.current_scene], Scene):
                        # Handle key events for scenes
                        if event.key == pg.K_SPACE or event.key == pg.K_RETURN:  
                            self.scenes[self.current_scene].next_dialogue()
                        elif event.key == pg.K_DOWN:
                            self.scenes[self.current_scene].next_choice()
                        elif event.key == pg.K_UP:
                            self.scenes[self.current_scene].prev_choice()
                    else:
                        self.scenes[self.current_scene].keydown(event.key)

                # Handle mouse events for scenes
                if isinstance(self.scenes[self.current_scene], Scene):
                    if event.type == pg.MOUSEBUTTONDOWN:
                        self.scenes[self.current_scene].check_mouse_choice(*event.pos)
                    if event.type == pg.MOUSEMOTION:
                        self.scenes[self.current_scene].hover_mouse_choice(*event.pos)

    def render_stuff_loop(self, dt):
        # Render the appropriate screen based on whether the start screen is active
        if self.isStartScreen:
            self.startScreen.render()
        else:
            self.screen.fill((255, 255, 255))  # Fill screen with white color
            
            # Update the current scene if finished
            if self.scenes[self.current_scene].is_finished():
                self.current_scene = min(self.current_scene + 1, len(self.scenes) - 1)

            # Render the current scene
            if isinstance(self.scenes[self.current_scene], Scene):
                self.scenes[self.current_scene].render()
            else:
                self.scenes[self.current_scene].render(dt)

    def mainLoop(self):
        # Main game loop
        while self.running:
            dt = self.clock.tick(60) / 1000  # Calculate delta time for frame rate control

            # Check if the start screen is still running
            self.isStartScreen = self.startScreen.check_running()

            self.handle_events()  # Handle user input events
            self.render_stuff_loop(dt)  # Render the game content
            pg.display.update()  # Update the display

if __name__ == "__main__":
    # Create a Game instance and start the main loop
    game = Game()
    game.mainLoop()
    pg.quit()  # Quit Pygame when the game ends
