a = ["ram is a good boy"]
a_list= a[0].split()
to_count = 0
for word in a_list:
    if len(word)>to_count:
        to_count = len(word)
print(f"word"to_count)

