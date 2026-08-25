<div align="center">

<br/>

<!-- Animated Typing Banner -->
<img
  src="https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=700&size=36&pause=1000&color=00D4FF&center=true&vCenter=true&width=760&lines=%F0%9F%A7%AE+Simple+Calculator;Python+%7C+Clean+%7C+Modular"
  alt="Typing SVG"
/>

<br/>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Level-1%20Project-00D4FF?style=for-the-badge&logo=rocket&logoColor=white" alt="Level 1"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="License"/>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge&logo=checkmarx&logoColor=white" alt="Status"/>
  <img src="https://img.shields.io/badge/Internship-CodVeda-FF6B6B?style=for-the-badge&logo=graduation-cap&logoColor=white" alt="CodVeda"/>
</p>

<br/>

> **A clean, modular Python calculator built as part of the CodVeda Python Internship — Level 1.**  
> Demonstrates core Python fundamentals: functions, error handling, and module design.

<br/>

---

</div>

## 📋 Table of Contents

- [✨ Overview](#-overview)
- [⚙️ Features](#️-features)
- [📁 Project Structure](#-project-structure)
- [🔧 Functions Reference](#-functions-reference)
- [🚀 Getting Started](#-getting-started)
- [▶️ Usage](#️-usage)
- [🧪 Running Tests](#-running-tests)
- [📊 Sample Output](#-sample-output)
- [🛡️ Error Handling](#️-error-handling)
- [🧠 What I Learned](#-what-i-learned)
- [📜 License](#-license)
- [👤 Author](#-author)

---

## ✨ Overview

The **Simple Calculator** is a beginner-friendly Python project that implements the four fundamental arithmetic operations — **addition**, **subtraction**, **multiplication**, and **division** — using clean, well-commented, and modular functions.

This project is part of **Level 1** of the **CodVeda Python Internship**, designed to strengthen the foundation of Python programming through hands-on tasks.

---

## ⚙️ Features

| Feature | Description |
|---|---|
| ➕ **Addition** | Computes the sum of two numbers |
| ➖ **Subtraction** | Computes the difference of two numbers |
| ✖️ **Multiplication** | Computes the product of two numbers |
| ➗ **Division** | Computes the quotient with zero-division protection |
| 🛡️ **Error Handling** | Gracefully handles `ZeroDivisionError` |
| 🔌 **Modular Design** | Functions are importable as a reusable module |
| 🧪 **Test File** | Includes a dedicated test script for validation |

---

## 📁 Project Structure

```
📦 Simple_Calculator/
├── 📄 calculator.py        # Core arithmetic functions + entry point
├── 🧪 test_calculator.py   # Standalone test/demo script
└── 📖 README.md            # Project documentation (you are here!)
```

---

## 🔧 Functions Reference

All arithmetic logic lives inside [`calculator.py`](./calculator.py):

<br/>

### `addition(a, b)` ➕

```python
def addition(a, b):
    # Returns Sum Of Two Numbers
    return a + b
```

> Returns the **sum** of `a` and `b`.

---

### `subtraction(a, b)` ➖

```python
def subtraction(a, b):
    # Returns Difference Of Two Numbers
    return a - b
```

> Returns the **difference** (`a - b`).

---

### `multiplication(a, b)` ✖️

```python
def multiplication(a, b):
    # Returns Product Of Two Numbers
    return a * b
```

> Returns the **product** of `a` and `b`.

---

### `division(a, b)` ➗

```python
def division(a, b):
    # Returns Quotient Of Two Numbers
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
```

> Returns the **quotient** (`a / b`). Safely handles division by zero.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have **Python 3.x** installed on your system.

```bash
# Check your Python version
python --version
```

### Clone the Repository

```bash
git clone https://github.com/HarsheyGolar/codveda-python-internship.git
cd codveda-python-internship/Level-1/Simple_Calculator
```

---

## ▶️ Usage

### Run the Calculator Directly

```bash
python calculator.py
```

### Import as a Module in Your Own Script

```python
from calculator import addition, subtraction, multiplication, division

# Perform calculations
print(addition(10, 5))        # Output: 15
print(subtraction(10, 5))     # Output: 5
print(multiplication(10, 5))  # Output: 50
print(division(10, 5))        # Output: 2.0
print(division(10, 0))        # Output: Error: Division by zero is not allowed.
```

---

## 🧪 Running Tests

A dedicated test script [`test_calculator.py`](./test_calculator.py) is included to validate all functions:

```bash
python test_calculator.py
```

**What it tests:**

```python
from calculator import addition, subtraction, division, multiplication

print(addition(24, 24))      # ➕ Tests addition
print(subtraction(2, 4))     # ➖ Tests subtraction
print(division(3, 0))        # ➗ Tests zero-division handling
print(multiplication(4, 2))  # ✖️ Tests multiplication
```

---

## 📊 Sample Output

```
# Running: python calculator.py
5
-11
44
1.0

# Running: python test_calculator.py
48
-2
Error: Division by zero is not allowed.
8
```

---

## 🛡️ Error Handling

The `division()` function uses Python's `try...except` block to gracefully catch `ZeroDivisionError`:

```python
try:
    return a / b
except ZeroDivisionError:
    return "Error: Division by zero is not allowed."
```

> 💡 Instead of crashing the program, it prints a user-friendly error message and returns `None`.

---

## 🧠 What I Learned

Through this project, I practiced and solidified the following Python concepts:

- ✅ **Defining and calling functions** with parameters and return values
- ✅ **Exception handling** using `try` / `except` blocks
- ✅ **Modular programming** — writing reusable, importable functions
- ✅ **`__name__ == "__main__"`** guard for entry-point control
- ✅ **Code documentation** using inline comments
- ✅ **Writing test scripts** to validate module behavior

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](../../LICENSE) file for details.

```
MIT License — Copyright (c) 2026 Harshey Golar
```

---

## 👤 Author

<div align="center">

### **Harshey Golar**
*Python Intern @ CodVeda Technologies — Level 1*

<br/>

[![GitHub](https://img.shields.io/badge/GitHub-HarsheyGolar-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/HarsheyGolar)

<br/>

---

<sub>⭐ If you found this project helpful, consider giving it a star!</sub>

<br/>

*Made with ❤️ and Python during the CodVeda Technologies Python Developer Internship*

</div>
