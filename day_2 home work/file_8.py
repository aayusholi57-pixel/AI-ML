# Sum of numbers from 1 to 4
total = 0
for i in range(1, 5):
    total = total + i
print(total)


# Print numbers in decreasing order
n = 5
while n > 0:
    print(n, end=" ")
    n = n - 2

print()  # Move to the next line


# Build a word in reverse
word = ""
for c in "abc":
    word = c + word
    print(word)