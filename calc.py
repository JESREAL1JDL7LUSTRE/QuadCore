class Calculator:
    def add(self, a, b):
        return a + b

# Instantiate the class
calc = Calculator()

while True:
    print("\n1-add")
    choice = input("function: ")

    if choice == '5':
        print("Exiting calculator. Goodbye!")
        break

    if choice in ('1'):
        try:
            num1 = float(input("select number 1: "))
            num2 = float(input("select number 2: "))

            if choice == '1':
                print(f"Sum: {calc.add(num1, num2)}")
        except ValueError:
            print("Invalid input! Please enter numerical values.")
    else:
        print("Invalid choice. Please select 1-5.")