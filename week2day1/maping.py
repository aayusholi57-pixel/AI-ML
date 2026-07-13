def word_length_dict(words):
    return {word: len(word) for word in words}

words = input("Enter words separated by space: ").split()

result = word_length_dict(words)
print("Dictionary:", result)