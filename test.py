import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 24

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Visual Adventure Game")

# Load font
font = pygame.font.Font(None, FONT_SIZE)

# Character class
class Character:
    def __init__(self, name, sprite_sheet, position):
        self.name = name
        self.sprite_sheet = sprite_sheet
        self.position = position
        self.frame = 0
        self.frames = self.load_frames()
        self.animation_speed = 0.1
        self.animation_timer = 0

    def load_frames(self):
        frames = []
        sheet_width, sheet_height = self.sprite_sheet.get_size()
        sprite_width = sheet_width // 3  # Assuming 3 frames in the sprite sheet
        for i in range(3):
            frame = self.sprite_sheet.subsurface((i * sprite_width, 0, sprite_width, sheet_height))
            frames.append(frame)
        return frames

    def update(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame = (self.frame + 1) % len(self.frames)

    def render(self, screen):
        screen.blit(self.frames[self.frame], self.position)

# Scene class
class Scene:
    def __init__(self, dialogues, characters):
        self.dialogues = dialogues
        self.current_dialogue = 0
        self.characters = characters

    def render(self, screen):
        screen.fill(WHITE)
        for character in self.characters:
            character.render(screen)
        if self.current_dialogue < len(self.dialogues):
            dialogue_surface = font.render(self.dialogues[self.current_dialogue], True, BLACK)
            screen.blit(dialogue_surface, (50, 50))

    def next_dialogue(self):
        self.current_dialogue += 1

    def is_finished(self):
        return self.current_dialogue >= len(self.dialogues)

    def update(self, dt):
        for character in self.characters:
            character.update(dt)

# Load assets
sprite_sheet = pygame.image.load('./res/icon.jpg').convert_alpha()

# Define characters
character1 = Character("Hero", sprite_sheet, (100, 300))

# Define scenes
scenes = [
    Scene(["Welcome to the game.", "This is the first scene."], [character1]),
    Scene(["This is the second scene.", "More dialogue here."], [character1]),
    # Add more scenes as needed
]

current_scene_index = 0

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(FPS) / 1000  # Delta time in seconds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Proceed to next dialogue on space bar
                scenes[current_scene_index].next_dialogue()
                if scenes[current_scene_index].is_finished():
                    current_scene_index += 1
                    if current_scene_index >= len(scenes):
                        running = False

    # Update current scene
    if current_scene_index < len(scenes):
        scenes[current_scene_index].update(dt)

    # Render current scene
    if current_scene_index < len(scenes):
        scenes[current_scene_index].render(screen)
    else:
        # Optionally, display a "The End" message
        screen.fill(WHITE)
        end_surface = font.render("The End", True, BLACK)
        screen.blit(end_surface, (SCREEN_WIDTH // 2 - end_surface.get_width() // 2, SCREEN_HEIGHT // 2 - end_surface.get_height() // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()
