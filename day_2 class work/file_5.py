score = 104
if score<0 or score>100:
    print("Invalid score")

elif score>=80:
    print(f"score: {score}, Grade: A")
elif score>=60:
    print(f"score: {score}, Grade: B")
elif score>=40:
    print(f"score: {score}, Grade: C")
else: 
    print("fail")
  