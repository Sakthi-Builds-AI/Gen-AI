# Grade System in Python

## Overview

This project is a simple Python program that converts a student's mark into a grade based on a predefined grading scale. The program accepts user input, validates the entered value, and displays the corresponding grade.

## Grading Scale

| Mark Range | Grade |
| ---------- | ----- |
| 90 - 100   | A     |
| 80 - 89    | B     |
| 70 - 79    | C     |
| 60 - 69    | D     |
| Below 60   | E     |

## Features

* Takes marks as input from the user.
* Assigns grades based on the grading scale.
* Validates that marks are within the range of 0 to 100.
* Handles invalid inputs gracefully.
* Uses only Python's standard library.

## Requirements

* Python 3.x

No third-party packages are required.

## How to Run

1. Clone this repository:

```bash
git clone <your-repository-url>
```

2. Navigate to the project folder:

```bash
cd <repository-name>
```

3. Run the program:

```bash
python grade_system.py
```

## Example Usage

### Valid Input

```text
Enter a mark (0-100): 85
Mark: 85.0
Grade: B
```

### Invalid Range

```text
Enter a mark (0-100): 120
Error: Mark must be between 0 and 100.
```

### Non-Numeric Input

```text
Enter a mark (0-100): hello
Error: Please enter a valid numeric mark.
```

## Learning Outcomes

* Understanding conditional statements (`if`, `elif`, `else`).
* Taking user input using the `input()` function.
* Validating user data.
* Handling errors using `try` and `except`.

## Author

Created as a Python programming exercise to demonstrate grading logic, input validation, and exception handling.
