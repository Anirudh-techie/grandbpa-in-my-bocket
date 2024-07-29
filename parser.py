import json

def get_scene_data():
    with open("./data.json") as f:
         data = json.load(f)
         print(data)
    pass


def get_dialogue_data(scene_index):
    with open("./data.json") as f:
            data = json.load(f)
            scenes = data["scenes"]
    pass

get_dialogue_data()


