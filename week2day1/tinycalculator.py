
def add(a, b):
    return a + b



def sub(a, b):
    return a - b



def mul(a, b):
    return a * b



def div(a, b):
    if b == 0:
        return "error occur"
    return a / b

print("Addition:", add(5, 5))
print("Subtraction:", sub(10, 5))
print("Multiplication:", mul(6, 5))
print("Division:", div(15, 3))
print("Division by zero:", div(3, 0))