class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b

# Instantiate the class
calc = Calculator()

while True:
    print("\n1-add, 2-substract, 3-multiply")
    choice = input("Select Operator: ")

    if choice == '5':
        print("Exiting calculator. Goodbye!")
        break

    if choice in ('1', '2', '3'):
        try:
            num1 = float(input("select number 1: "))
            num2 = float(input("select number 2: "))

            if choice == '1':
                print(f"Sum: {calc.add(num1, num2)}")
            elif choice == '2':
                print(f"Difference: {calc.substract(num1, num2)}")
            elif choice == '3':
                print(f"Product: {calc.multiply(num1, num2)}")
        except ValueError:
            print("Invalid input! Please enter numerical values.")
    else:
        print("Invalid choice. Please select 1-5.")