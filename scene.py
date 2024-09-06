from dialogue import Dialogue
from sprite import Sprite
class Scene:
    def __init__(self,screen, background, sprites, dialogues):
        self.background = background
        self.sprites = sprites
        self.dialogues = dialogues
        self.screen = screen

        self.currentDialogue = 0
        self.is_finished_bool = False

    def render(self):
        current_dialogue: Dialogue = self.dialogues[self.currentDialogue]
        self.screen.blit(self.background, (0, 0))
        

        for state in current_dialogue.sprite_states:
            sprite:Sprite = self.sprites[state]
            states = current_dialogue.sprite_states[state]
            if "position" in states:
                if "smooth" in states:
                     speed = states.get("speed", 1)
                     sprite.move_smooth(states["position"][0], states["position"][1], speed)
                else:
                    sprite.move(states["position"][0], states["position"][1])
            if "state" in states:
                sprite.set_state(states["state"])

            if "show" in states:
                sprite.set_visibility(states["show"])
            sprite.render()
            
        current_dialogue.render(self.screen)
        

    def next_dialogue(self):
       current_dialogue = self.dialogues[self.currentDialogue]
       self.currentDialogue += current_dialogue.go_next()
       if self.currentDialogue > len(self.dialogues) - 1:
           self.is_finished_bool = True
           return
    
    def next_choice(self):
        self.dialogues[self.currentDialogue].next_choice()
    
    def prev_choice(self):
        self.dialogues[self.currentDialogue].prev_choice()
    
    def check_mouse_choice(self, x, y):
        current_dialogue = self.dialogues[self.currentDialogue]
        choice = current_dialogue.get_hovered_choice(x, y)
        if choice != -1:
            self.currentDialogue+=current_dialogue.go_next(choice)
        
    
    def hover_mouse_choice(self, x, y):
        current_dialogue = self.dialogues[self.currentDialogue]
        choice = current_dialogue.get_hovered_choice(x, y)
        print(choice)

        if choice != -1:
            current_dialogue.choose(choice)
    
    def is_finished(self):
        return self.is_finished_bool