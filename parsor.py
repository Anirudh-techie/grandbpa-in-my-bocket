import json
from dialogue import Dialogue
import pygame
from scene import Scene
from game.gamescene import GameScene
from sprite import Sprite

def get_scene_data(screen)-> list[Scene]:
    with open("./data.json") as f:
         data = json.load(f)
         scenes = data["scenes"]
         sprites = data["sprites"]
         for s_id in sprites:
             sprites[s_id] = Sprite(screen, sprites[s_id]["name"], s_id )
            #  sprites[s_id] = None
         for i,scene in enumerate(scenes):
             if "game" in scene:
                  difficulty = scene["game"]["difficulty"]
                  scenes[i] = GameScene(screen,difficulty)
                  continue
             background = pygame.image.load(f'./res/backgrounds/{scene["bg"]}').convert()
             background = pygame.transform.scale(background, (800, 700))
             dialogues = get_dialogue_data(i)
             scenes[i] = Scene(screen, background, sprites, dialogues)
    return scenes


def get_dialogue_data(scene_index):
    with open("./data.json") as f:
            data = json.load(f)
            scene = data["scenes"][scene_index]
            ds = scene["dialogues"]
            dialogues = [Dialogue(d["text"],d.get("name"), d.get("choices",[]), d.get("sprite_states", {}), d.get("next_dialogue", 1))  for d in ds]
            return dialogues
    

