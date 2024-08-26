import pygame
from utils import lerp, wrap_multi_line
class Dialogue:
    def __init__(self, screen_width, screen_height, text:str, character_name:str, choices=[], sprite_states={}, next_dialogue=1):
        pygame.mixer.init()
        self.text_anim_sound  = pygame.mixer.Sound('res/soundfx/8-bit-loop-189494.mp3')
        self.text_anim_sound_playing = False
        self.screen_width, self.screen_height = screen_width, screen_height
        self.text_bg_width, self.text_bg_height = screen_width * 7/10, screen_height * 2.5/10
        self.text = text
        self.choices = choices
        self.sprite_states = sprite_states
        self.diaFont = pygame.font.Font("res/fonts/dia/CrimsonPro-VariableFont_wght.ttf", 26)
        self.nameFont = pygame.font.Font("res/fonts/blackpearl-font/Blackpearl-vPxA.ttf", 40)
        self.character_name = character_name
        self.current_choice = 0
        self.next_dialogue = next_dialogue

        self._animchar = 0
        self.textlen = len(text)

        self._choiceheight = 0
        self._choicepos = self.screen_height - self.text_bg_height - 30 - 76 - (max(0,len(self.choices) - 2) * 30)
        self._choice_opacity = 0
        self._chosen_bg_opacity = 0
        pass
    def render(self, screen):
        

        text_bg = pygame.Surface((self.text_bg_width, self.text_bg_height),pygame.SRCALPHA)
        pygame.draw.rect(text_bg, (255,255,255,210), text_bg.get_rect(), border_radius=20)
        screen.blit(text_bg, (self.screen_width/2 - self.text_bg_width/2 , self.screen_height - self.text_bg_height - 30))

   
        self._animchar += 1.4
        self._animchar = min(self.textlen, self._animchar)

        if not self.text_anim_sound_playing:
            self.text_anim_sound.stop()

        if int(self._animchar) > int(self._animchar - 0.7):
            if self.text_anim_sound_playing:
                self.text_anim_sound.play(1)
                self.text_anim_sound_playing = False
        else:
            self.text_anim_sound.stop()
            self.text_anim_sound_playing = True
            
        
        text = wrap_multi_line(self.text, self.diaFont, self.text_bg_width - 40)
        linesum = 0
        for i,line in enumerate(text):
            line_surface = self.diaFont.render(line[:max(0, int(self._animchar) - linesum)], True, (0,0,0))
            screen.blit(line_surface, (self.screen_width/2 - self.text_bg_width/2 + 20, self.screen_height - self.text_bg_height + i*20 + 30))
            linesum += len(line)
        

        name = self.nameFont.render(self.character_name, True, (0,0,200))
        screen.blit(name, (self.screen_width/2 - self.text_bg_width/2 + 15, self.screen_height - self.text_bg_height - 15))

        
        if self.choices:
            choice_mult = 0.95
            ideal_height = 96 + (max(0,len(self.choices) - 2) * 40)
            ideal_pos = self.screen_height - self.text_bg_height - 30 - ideal_height - 5

            self._choicepos = lerp(self._choicepos, ideal_pos, 0.2)
            self._choiceheight = lerp(self._choiceheight, ideal_height, 0.2)

            choice_bg = pygame.Surface((self.text_bg_width*choice_mult, int(self._choiceheight)),pygame.SRCALPHA)
            pygame.draw.rect(choice_bg, (255,255,255,210), (0,0,self.text_bg_width*choice_mult, self._choiceheight), border_radius=10)
            for i,choice in enumerate(self.choices):
                  self._chosen_bg_opacity = lerp(self._chosen_bg_opacity, 255, 0.05)
                  choice_text = self.diaFont.render(choice[0], True, (0,0,0))
                  chosen_bg = pygame.Surface((self.text_bg_width*choice_mult - 20, 35),pygame.SRCALPHA)
                  chosen_bg.fill((0,0,0,0))
                  if i == self.current_choice:
                      pygame.draw.rect(chosen_bg, (255, 0, 0, self._chosen_bg_opacity), chosen_bg.get_rect(), border_radius=5)
                  chosen_bg.blit(choice_text, (10,2))

                  if self._choiceheight >= ideal_height:
                     self._choice_opacity += 15 * (self._choice_opacity <= 255*len(self.choices))
                     chosen_bg.set_alpha(max(0, self._choice_opacity - (255*i)))
                     choice_bg.blit(chosen_bg, (8, i*35 + 8))
            screen.blit(choice_bg, (self.screen_width/2 - self.text_bg_width*choice_mult/2, self._choicepos)) 
                  

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

        
