# grade_system.py
try:
    mark = float(input("Enter a mark (0-100): "))

    if mark < 0 or mark > 100:
        print("Error: Mark must be between 0 and 100.")
    elif mark >= 90:
        grade = "A"
    elif mark >= 80:
        grade = "B"
    elif mark >= 70:
        grade = "C"
    elif mark >= 60:
        grade = "D"
    else:
        grade = "E"

    if 0 <= mark <= 100:
        print(f"Mark: {mark}")
        print(f"Grade: {grade}")

except ValueError:
    print("Error: Please enter a valid numeric mark.")
