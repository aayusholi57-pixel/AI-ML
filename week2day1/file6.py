def get_squares():
    squares = []
    for n in range(5):
        squares.append(n * n)
    return squares

result = get_squares()
print(result)