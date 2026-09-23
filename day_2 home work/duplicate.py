word = "dondai"
remove_duplicate=""
for char in word:
    if char not in remove_duplicate:
        remove_duplicate+=char

print("Original string:", word)
print("String after removing duplicates:", remove_duplicate)