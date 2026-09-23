a = "ram,ram,ram,shyam,shyam"

words = a.split(",")
b = set(words)

for key in b:
    count = 0
    for word in words:
        if key == word:
            count += 1
    print(f"{key}: {count}")