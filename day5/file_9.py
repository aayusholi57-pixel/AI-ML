words = ["ram", "ram", "ram", "shyam", "shyam"]
counts = {}

for word in words:
    if word not in counts:
        counts[word] = 0
    counts[word] += 1

for key, value in counts.items():
    print(f"{key}: {value}")
