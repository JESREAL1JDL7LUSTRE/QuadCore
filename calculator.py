class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            return "Cannot divide by zero!"
        return a/b

# Instantiate the class
calc = Calculator()

while True:
    print("\n1-Add, 2-Substract, 3-Multiply, 4-Divide, 5-Exit")
    choice = input("Select Operator: ")

    if choice == '5':
        print("Exiting calculator. Goodbye!")
        break

    if choice in ('1', '2', '3', '4', '5'):
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if choice == '1':
                print(f"Sum: {calc.add(num1, num2)}")
            elif choice == '2':
                print(f"Difference: {calc.substract(num1, num2)}")
            elif choice == '3':
                print(f"Product: {calc.multiply(num1, num2)}")
            elif choice == '4':
                print(f"Quotient: {calc.divide(num1, num2)}")
        except ValueError:
            print("Invalid input! Please enter numerical values.")
    else:
        print("Invalid choice. Please select 1-5.")