import json

f = open('papers.json')

data = json.load(f)

print(len(data["Artificial Intelligence"]))