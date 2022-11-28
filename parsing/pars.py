import json

with open('config.json', 'r', encoding='utf-8') as f:
    lands = json.load(f)

print (lands)

for buildings, resourses in lands.items():
    print(buildings)
    print('\n'.join(resourses)) 
