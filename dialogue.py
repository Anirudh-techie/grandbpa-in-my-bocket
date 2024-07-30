import pygame

class Dialogue:
    def __init__(self, text:str, character_name:str, choices=[], sprite_states={}):
        self.text = text
        self.choices = choices
        self.sprite_states = sprite_states
        self.diaFont = pygame.font.Font(None, 25)
        self.nameFont = pygame.font.Font(None, 32)
        self.character_name = character_name
        self.current_choice = 0
        pass
    def render(self, screen):
        

        text_bg = pygame.Surface((500, 160),pygame.SRCALPHA)
        text_bg.fill((255,255,255,200))
        screen.blit(text_bg, (150, 530))

        text = self.diaFont.render(self.text, True, (0,0,0))
        screen.blit(text, (160, 570))

        name = self.nameFont.render(self.character_name, True, (0,0,0))
        screen.blit(name, (160, 540))

        
        if self.choices:
            choice_bg = pygame.Surface((500, 90 + (max(0,len(self.choices) - 2) * 30)),pygame.SRCALPHA)
            choice_bg.fill((255,255,255,210))
            screen.blit(choice_bg, (150, 430 - (max(0,len(self.choices) - 2) * 30))) 
            for i,choice in enumerate(self.choices):
                if i == self.current_choice:
                    chosen_bg = pygame.Surface((500, 30),pygame.SRCALPHA)
                    chosen_bg.fill((255,0,0,255))
                    screen.blit(chosen_bg, (150, 438 - (max(0,len(self.choices) - 2) * 30) + i*30))
                choice_text = self.diaFont.render(choice, True, (0,0,0))
                screen.blit(choice_text, (160, 430 - (max(0,len(self.choices) - 2) * 30) + i*30 + 15))

    def next_choice(self):
        self.current_choice += 1
        self.current_choice %= len(self.choices)
    
    def prev_choice(self):
        self.current_choice -= 1
        self.current_choice %= len(self.choices)