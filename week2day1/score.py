def subject(math, english, nepali, science):
    if math >= 40 and english >= 40 and nepali >= 40 and science >= 40:
        return "Pass"
    else:
        return "Fail"

result = subject(70, 65, 80, 55)

print("Math:", 70)
print("English:", 65)
print("Nepali:", 80)
print("Science:", 55)
print("Result:", result)