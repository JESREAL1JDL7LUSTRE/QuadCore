from concurrent.futures import ProcessPoolExecutor

employees = [
    ("Alice", 25000),
    ("Bob", 32000),
    ("Charlie", 28000),
    ("Diana", 40000),
    ("Edward", 35000)
]

def compute_total_deduction(employee):
    name, salary = employee
    total = salary * (0.045 + 0.025 + 0.02 + 0.10)
    net_salary = salary - total
    return name, salary, total, net_salary


if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        results = executor.map(compute_total_deduction, employees)

    for name, salary, total, net in results:
        print(f"\nEmployee: {name}")
        print(f"Gross Salary: {salary}")
        print(f"Total Deduction: {total:.2f}")
        print(f"Net Salary: {net:.2f}")
