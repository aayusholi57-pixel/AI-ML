class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def hello(self):
        print(self.name, "hello")


s = Student("Aayush", 31)
print(s.name)