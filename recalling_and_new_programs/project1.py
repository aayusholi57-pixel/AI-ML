print("=" * 40)
print("      STUDENT MANAGEMENT SYSTEM")
print("=" * 40)

students = []

num = int(input("How many students do you want to add? "))

# -----------------------------
# Add Students
# -----------------------------
for i in range(num):
    print(f"\nEnter details of Student {i+1}")

    name = input("Name   : ").strip()
    rollno = int(input("Roll No: "))
    course = input("Course : ").strip()
    marks = float(input("Marks  : "))

    if marks >= 40:
        status = "PASS"
    else:
        status = "FAIL"

    student = {
        "name": name,
        "rollno": rollno,
        "course": course,
        "marks": marks,
        "status": status
    }

    students.append(student)

print("\n" + "=" * 40)
print("ALL STUDENTS")
print("=" * 40)

# -----------------------------
# Display All Students
# -----------------------------
for s in students:
    print(f"""
Name   : {s['name']}
Roll   : {s['rollno']}
Course : {s['course']}
Marks  : {s['marks']}
Status : {s['status']}
------------------------------
""")

# -----------------------------
# Search Student by Name
# -----------------------------
print("\nSEARCH STUDENT")

query = input("Enter student name: ").strip().lower()

found = False

for s in students:
    if s["name"].lower() == query:
        print("\nStudent Found")
        print(f"Name   : {s['name']}")
        print(f"Roll   : {s['rollno']}")
        print(f"Course : {s['course']}")
        print(f"Marks  : {s['marks']}")
        print(f"Status : {s['status']}")
        found = True

if not found:
    print("Student not found.")

# -----------------------------
# Show Only Passed Students
# -----------------------------
print("\nPASSED STUDENTS")

for s in students:
    if s["status"] == "PASS":
        print(f"{s['name']} ({s['marks']})")

# -----------------------------
# Calculate Average Marks
# -----------------------------
total = 0

for s in students:
    total += s["marks"]

average = total / len(students)

print(f"\nAverage Marks = {average:.2f}")

# -----------------------------
# Highest Scorer
# -----------------------------
highest = students[0]

for s in students:
    if s["marks"] > highest["marks"]:
        highest = s

print("\nHIGHEST SCORER")
print(f"Name  : {highest['name']}")
print(f"Marks : {highest['marks']}")

# -----------------------------
# Count Pass and Fail
# -----------------------------
pass_count = 0
fail_count = 0

for s in students:
    if s["status"] == "PASS":
        pass_count += 1
    else:
        fail_count += 1

print("\nRESULT SUMMARY")
print(f"Pass Students : {pass_count}")
print(f"Fail Students : {fail_count}")

# -----------------------------
# Lowest Scorer
# -----------------------------
lowest = students[0]

for s in students:
    if s["marks"] < lowest["marks"]:
        lowest = s

print("\nLOWEST SCORER")
print(f"Name  : {lowest['name']}")
print(f"Marks : {lowest['marks']}")

# -----------------------------
# Topper List
# -----------------------------
print("\nTOPPER(S)")

highest_marks = highest["marks"]

for s in students:
    if s["marks"] == highest_marks:
        print(f"{s['name']} ({s['marks']})")