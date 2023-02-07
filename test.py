import json

with open("test.json", "r+",encoding='utf-8') as f:
    data=json.loads(f.read())
    for i in data:
        print(i['id'])