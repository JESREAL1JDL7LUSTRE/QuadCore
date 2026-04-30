from concurrent.futures import ThreadPoolExecutor
import threading

# Deduction functions
def compute_sss(salary):
    return salary * 0.045

def compute_philhealth(salary):
    return salary * 0.025

def compute_pagibig(salary):
    return salary * 0.02

def compute_tax(salary):
    return salary * 0.10


employees = [
    ("Alice", 25000),
    ("Bob", 32000),
    ("Charlie", 28000),
    ("Diana", 40000),
    ("Edward", 35000)
]


for name, salary in employees:
    with ThreadPoolExecutor() as executor:
        future_sss = executor.submit(compute_sss, salary)
        future_ph = executor.submit(compute_philhealth, salary)
        future_pg = executor.submit(compute_pagibig, salary)
        future_tax = executor.submit(compute_tax, salary)

        sss = future_sss.result()
        philhealth = future_ph.result()
        pagibig = future_pg.result()
        tax = future_tax.result()

    total_deduction = sss + philhealth + pagibig + tax

    print(f"\nEmployee: {name}")
    print(f"Gross Salary: {salary}")
    print(f"SSS: {sss:.2f}")
    print(f"PhilHealth: {philhealth:.2f}")
    print(f"Pag-IBIG: {pagibig:.2f}")
    print(f"Tax: {tax:.2f}")
    print(f"Total Deduction: {total_deduction:.2f}")
