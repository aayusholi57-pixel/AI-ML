a= "ram,ram,ram,shyam,shyam"
b= set(a.split(","))
for key in b:
    for word in a:
        if key == word:
            count += 1
print(f"{key}: {count}")