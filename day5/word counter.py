text = "ram,ram,ram,shyam,shyam"
words = text.split(",")
counts = {}

for word in words:
    counts[word] = counts.get(word, 0) + 1

for key, count in counts.items():
    print(f"{key}: {count}")
