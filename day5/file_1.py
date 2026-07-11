a= {"name": "John", "age": 30, "city": "New York"}
to_print = a["name"]
print(to_print)
a["age"]=45
print(a["age"])
print(a.get("agee")) 

if a.get("agee"):
    print(f"your age is  {a.get('age')}")
