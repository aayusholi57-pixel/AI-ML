a=["ram","ram","ram","shyam","shyam"]
b=set(a)
dict={"ram":0,"shyam":0}
for key in b:
    for word in a:
        if key==word:
            dict[key]+=1

for key, value in dict.items():
    print(f"{key}: {value}")