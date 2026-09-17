a = ["ram is a good boy"]
a_list = a[0].split()
longest_word_length = 0

for word in a_list:
    if len(word) > longest_word_length:
        longest_word_length = len(word)

print("Longest word length:", longest_word_length)
