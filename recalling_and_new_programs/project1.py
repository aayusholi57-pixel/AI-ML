print("=" * 40)
print("      STUDENT MANAGEMENT SYSTEM")
print("=" * 40)

students = []

while True:
    try:
        num = int(input("How many students do you want to add? "))
        if num > 0:
            break
        print("Please enter at least 1 student.")
    except ValueError:
        print("Please enter a valid whole number.")

# -----------------------------
# Add Students
# -----------------------------
for i in range(num):
    print(f"\nEnter details of Student {i + 1}")

    name = input("Name   : ").strip()
    rollno = int(input("Roll No: "))
    course = input("Course : ").strip()

    while True:
        try:
            marks = float(input("Marks  : "))
            if 0 <= marks <= 100:
                break
            print("Marks must be between 0 and 100.")
        except ValueError:
            print("Please enter a valid number for marks.")

    status = "PASS" if marks >= 40 else "FAIL"

    student = {
        "name": name,
        "rollno": rollno,
        "course": course,
        "marks": marks,
        "status": status,
    }

    students.append(student)

print("\n" + "=" * 40)
print("ALL STUDENTS")
print("=" * 40)

# -----------------------------
# Display All Students
# -----------------------------
for student in students:
    print(f"""
Name   : {student['name']}
Roll   : {student['rollno']}
Course : {student['course']}
Marks  : {student['marks']}
Status : {student['status']}
------------------------------
""")

# -----------------------------
# Search Student by Name
# -----------------------------
print("\nSEARCH STUDENT")

query = input("Enter student name: ").strip().lower()
found = False

for student in students:
    if student["name"].lower() == query:
        print("\nStudent Found")
        print(f"Name   : {student['name']}")
        print(f"Roll   : {student['rollno']}")
        print(f"Course : {student['course']}")
        print(f"Marks  : {student['marks']}")
        print(f"Status : {student['status']}")
        found = True

if not found:
    print("Student not found.")

# -----------------------------
# Show Only Passed Students
# -----------------------------
print("\nPASSED STUDENTS")

for student in students:
    if student["status"] == "PASS":
        print(f"{student['name']} ({student['marks']})")

# -----------------------------
# Calculate Average Marks
# -----------------------------
total = sum(student["marks"] for student in students)
average = total / len(students)
print(f"\nAverage Marks = {average:.2f}")

# -----------------------------
# Highest and Lowest Scorers
# -----------------------------
highest = max(students, key=lambda student: student["marks"])
lowest = min(students, key=lambda student: student["marks"])

print("\nHIGHEST SCORER")
print(f"Name  : {highest['name']}")
print(f"Marks : {highest['marks']}")

print("\nLOWEST SCORER")
print(f"Name  : {lowest['name']}")
print(f"Marks : {lowest['marks']}")

# -----------------------------
# Count Pass and Fail
# -----------------------------
pass_count = sum(student["status"] == "PASS" for student in students)
fail_count = len(students) - pass_count

print("\nRESULT SUMMARY")
print(f"Pass Students : {pass_count}")
print(f"Fail Students : {fail_count}")

# -----------------------------
# Topper List
# -----------------------------
print("\nTOPPER(S)")

highest_marks = highest["marks"]
for student in students:
    if student["marks"] == highest_marks:
        print(f"{student['name']} ({student['marks']})")
