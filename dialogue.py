import pygame
from utils import lerp, wrap_multi_line
class Dialogue:
    def __init__(self, text:str, character_name:str, choices=[], sprite_states={}, next_dialogue=1):
        self.text = text
        self.choices = choices
        self.sprite_states = sprite_states
        self.diaFont = pygame.font.Font(None, 25)
        self.nameFont = pygame.font.Font(None, 32)
        self.character_name = character_name
        self.current_choice = 0
        self.next_dialogue = next_dialogue

        self._animchar = 0
        self.textlen = len(text)

        self._choiceheight = 0
        self._choicepos = 450 - (max(0,len(self.choices) - 2) * 30) + 76 + (max(0,len(self.choices) - 2) * 30)
        self._choice_opacity = 0
        self._chosen_bg_opacity = 0
        pass
    def render(self, screen):
        

        text_bg = pygame.Surface((500, 160),pygame.SRCALPHA)
        text_bg.fill((255,255,255,200))
        screen.blit(text_bg, (150, 530))

   
        self._animchar += 1.4
        self._animchar = min(self.textlen, self._animchar)

        if int(self._animchar) > int(self._animchar - 0.7):
            pass #add sound here
        
        text = wrap_multi_line(self.text, self.diaFont, 500)
        linesum = 0
        for i,line in enumerate(text):
            line_surface = self.diaFont.render(line[:max(0, int(self._animchar) - linesum)], True, (0,0,0))
            screen.blit(line_surface, (160, 570 + i*20))
            linesum += len(line)
        

        name = self.nameFont.render(self.character_name, True, (0,0,0))
        screen.blit(name, (160, 540))

        
        if self.choices:
            ideal_height = 76 + (max(0,len(self.choices) - 2) * 30)
            ideal_pos = 450 - (max(0,len(self.choices) - 2) * 30)

            self._choicepos = lerp(self._choicepos, ideal_pos, 0.2)
            self._choiceheight = lerp(self._choiceheight, ideal_height, 0.2)

            choice_bg = pygame.Surface((500, int(self._choiceheight)),pygame.SRCALPHA)
            choice_bg.fill((255,255,255,210))

            for i,choice in enumerate(self.choices):
                  self._chosen_bg_opacity = lerp(self._chosen_bg_opacity, 255, 0.05)
                  choice_text = self.diaFont.render(choice[0], True, (0,0,0))
                  chosen_bg = pygame.Surface((480, 30),pygame.SRCALPHA)
                  chosen_bg.fill((0,0,0,0))
                  if i == self.current_choice:
                      chosen_bg.fill((255,0,0,self._chosen_bg_opacity))
                  chosen_bg.blit(choice_text, (10,8))

                  if self._choiceheight >= ideal_height:
                     self._choice_opacity += 15 * (self._choice_opacity <= 255*len(self.choices))
                     chosen_bg.set_alpha(max(0, self._choice_opacity - (255*i)))
                     choice_bg.blit(chosen_bg, (8, i*30 + 8))
            screen.blit(choice_bg, (150, self._choicepos)) 
                  

    def next_choice(self):
        self.current_choice += 1
        self.current_choice %= len(self.choices)
        self._chosen_bg_opacity = 0
    
    def prev_choice(self):
        self.current_choice -= 1
        self.current_choice %= len(self.choices)
        self._chosen_bg_opacity = 0


    def go_next(self, choice=None):
         if choice == None:
               choice = self.current_choice
         if self.choices:
            next_dialogue = self.choices[choice][1]
         else:
            next_dialogue = self.next_dialogue
         return next_dialogue
    def choose(self, choice):
        self._chosen_bg_opacity = 0 if self.current_choice != choice else 255
        self.current_choice = choice

        
