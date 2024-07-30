class Scene:
    def __init__(self,screen, background, sprites, dialogues):
        self.background = background
        self.sprites = sprites
        self.dialogues = dialogues
        self.screen = screen

        self.currentDialogue = 0

    def render(self):
        current_dialogue = self.dialogues[self.currentDialogue]
        self.screen.blit(self.background, (0, 0))
        current_dialogue.render(self.screen)

    def next_dialogue(self):
       self.currentDialogue += 1
    
    def next_choice(self):
        self.dialogues[self.currentDialogue].next_choice()
    
    def prev_choice(self):
        self.dialogues[self.currentDialogue].prev_choice()

    def check_mouse_choice(self, x, y):
        current_dialogue = self.dialogues[self.currentDialogue]
        if current_dialogue.choices:
            for i,choice in enumerate(current_dialogue.choices):
                if 150 < x < 650 and 430 - (max(0,len(current_dialogue.choices) - 2) * 30) + i*30 < y < 430 - (max(0,len(current_dialogue.choices) - 2) * 30) + i*30 + 30:
                    print(i)
        return -1
    