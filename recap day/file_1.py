'''name = "Aayush oli"
age = 20
print(type(name),type(age))

age = 0
print(bool(age))

name = "Aayush"
age = "20"
print(name + age)


mark = 34
grade = "A"
if mark >= 30 : 
       print(f"the person have acheieved mark{mark}and gradeis {grade}")

else: 
       print(f"i dont know")

       num = 33
if num % 3 == 0: 
    print(f"true")
else: 
    print(f"false")

    
    num = 33
a = int(input("enter a number:"))
if a == num // 2: 
    print(f"{a}is correct")
    print(bool(num))
else:
    print("nothing")



    a = input("Enter name of a person: ")

print(a.strip())
print(a.strip().upper())

print("o,l,i".split(","))
print("oli".replace("o", "i"))

print(f"Your results are: {a.strip()}, {a.strip().upper()}")

a= input("enter your name:")
print(a.strip())
print(a.strip().title())
print(a.split(","))
print(a.replace("o","i"))



a = input("enter your name:")
a.split()
count = 0
for letter in a.lower():
    if letter in "aeiou":
        count+=1


print(f"volwel letter: {count}")



a = input("enter the word:")

a.split()

count = 0

for letter in a.lower():
    if letter.isalpha() and letter not in "aeiou":
        count+=1
print(f"number of consonant is : {count}")


age= int(input("enter the age:"))
while age>18:
    print(f"current age: {age}- 18")
    age = age -1 
    print("next")



'''






