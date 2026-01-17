def calculate(a, op, b):
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        if b == 0:
            return "cannot divide by zero"
        return a / b
    
while True:
    n1 = input("\nEnter the 1st Number (or q to quit): ")
    if n1 == "q":
        break
    try:
        n1 = float(n1)
    except:
        print("invalid Number")
        continue