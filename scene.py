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
        current_dialogue.render(self.screen)

        for state in current_dialogue.sprite_states:
            sprite:Sprite = self.sprites[state]
            states = current_dialogue.sprite_states[state]
            if "position" in states:
                sprite.move_smooth(states["position"][0], states["position"][1])
            # sprite.move_smooth(newx, newy)
            if "state" in states:
                sprite.set_state(states["state"])

            if "show" in states:
                sprite.set_visibility(states["show"])
            sprite.render()
            # if
        

    def next_dialogue(self):
       current_dialogue = self.dialogues[self.currentDialogue]
       if self.currentDialogue == len(self.dialogues) - 1:
           self.is_finished_bool = True
           return
       self.currentDialogue += current_dialogue.go_next()
    
    def next_choice(self):
        self.dialogues[self.currentDialogue].next_choice()
    
    def prev_choice(self):
        self.dialogues[self.currentDialogue].prev_choice()

    def check_mouse_choice(self, x, y):
        current_dialogue = self.dialogues[self.currentDialogue]
        if current_dialogue.choices:
            base_y = 450 - max(0, len(current_dialogue.choices) - 2) * 30

            for i in range(len(current_dialogue.choices)):
               if 160 <= x <= 650 and base_y + i * 30 <= y <= base_y + i * 30 + 30:
                     self.currentDialogue+=current_dialogue.go_next(i)
        return -1
    
    def hover_mouse_choice(self, x, y):
         current_dialogue = self.dialogues[self.currentDialogue]
         if current_dialogue.choices:
            base_y = 450 - max(0, len(current_dialogue.choices) - 2) * 30

            for i in range(len(current_dialogue.choices)):
               if 160 <= x <= 650 and base_y + i * 30 <= y <= base_y + i * 30 + 30:
                     current_dialogue.choose(i)

         return -1
    
    def is_finished(self):
        return self.is_finished_bool