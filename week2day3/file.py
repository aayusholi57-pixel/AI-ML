import json

data={"name": "aayush", "student":False}

json_example = json.dumps(data, indent=2)

print(json_example)

print(type(json_example))

json_string= '{"name":"Aayush","isStudent": false}'
print(type(json.loads(json_string)))
print(json.loads(json_string))