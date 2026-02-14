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
