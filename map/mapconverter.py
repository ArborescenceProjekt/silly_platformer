import json


with open("map.json") as file:
    data = json.load(
        file
    )


collider_layer = data['layers'][0]
objects = collider_layer['objects']

level_data = {
    "colliders": []
}

for obj in objects:
    level_data['colliders'].append(
        (
            obj['x'], obj['y'], 
            obj['width'], obj['height'], 
        )
    )


with open('level.json', 'w') as file:
    json.dump(
        level_data,
        file,
        indent=4
    )