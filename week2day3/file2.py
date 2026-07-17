import json

with open("data/user.json") as f:
    data = json.load(f)

print(type(data))
print(data)

test_dict = {"name":"harry","age":21}

with open("data/user_2.json","w")as f:
    json.dump(test_dict,f,indent=2)

