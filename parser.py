import json
from dialogue import Dialogue
import pygame
def get_scene_data():
    with open("./data.json") as f:
         data = json.load(f)
         scenes = data["scenes"]
         for i,scene in enumerate(scenes):
             background = pygame.image.load(scene["background"]).convert()
             dialogues = get_dialogue_data(i)
             
    pass


def get_dialogue_data(scene_index):
    with open("./data.json") as f:
            data = json.load(f)
            scene = data["scenes"][scene_index]
            ds = scene["dialogues"]
            dialogues = [Dialogue(d["text"], d.get("choices",[]), d.get("sprite_states", {}))  for d in ds]
            return dialogues
    

get_dialogue_data(0)

