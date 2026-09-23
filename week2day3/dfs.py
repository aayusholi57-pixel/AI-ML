from pathlib import Path

# Write three lines
with open("notes.txt", "w") as file:
    file.write("Python is easy to learn.\n")
    file.write("Practice makes perfect.\n")
    file.write("Files help store data.\n")

# Append one more line
with open("notes.txt", "a") as file:
    file.write("This is the fourth line.\n")

path = Path("notes.txt")

if path.exists():
    try:
        with open("notes.txt", "r") as file:
            content = file.read()
            print("Contents of notes.txt:")
            print(content)

        with open("notes.txt", "r") as file:
            lines = file.readlines()

        count = sum(1 for line in lines if line.strip())
        print("Number of non-empty lines:", count)

    except FileNotFoundError:
        print("File not found.")
else:
    print("notes.txt does not exist.")