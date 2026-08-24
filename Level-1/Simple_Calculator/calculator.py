def addition(a, b):
    # Returns Sum Of Two Nummbers....
    return a + b

def subtraction(a, b):
    # Returns Difference Of Two Numbers....
    return a - b

def multiplication(a, b):
    # Returns Product Of Two Numbers....
    return a * b

def division(a, b):
    # Returns Quotient Of Two Numbers....
    try:
        return a/b
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."

def main():
    # Get Two Numbers From the User.
    a = int(input("Enter a number: "))
    b = int(input("Enter a number: "))

    # Display the available arithmetic operations.
    print("\nChoose the Operation.")
    print("1. Addition(+)")
    print("2. Subtraction(-)")
    print("3. Multiplication(×)")
    print("4. Division(÷)")

    # Read the user's operation choice.
    choice = input("Enter Your Choice (1/2/3/4): ")

    # Execute the selected operation.
    if choice == "1":
        print(addition(a, b))
    elif choice == "2":
        print(subtraction(a, b))
    elif choice == "3":
        print(multiplication(a, b))
    elif choice == "4":
        print(division(a, b))
         # Handle invalid operation selections.
    else:
        print(f"Invalid choice! Please select a valid operation menu number: {choice}")

if __name__=="__main__": main()