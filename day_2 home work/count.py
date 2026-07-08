word = "kaley loves junu"

vowels = "aeiouAEIOU"

vowel_count = 0
consonant_count = 0
space_count = 0
special_count = 0

for char in word:
    if char in vowels:
        vowel_count += 1
    elif char.isalpha():
        consonant_count += 1
    elif char == " ":
        space_count += 1
    else:
        special_count += 1

print("Total characters :", len(word))
print("Vowels           :", vowel_count)
print("Consonants       :", consonant_count)
print("Spaces           :", space_count)
print("Special chars    :", special_count)