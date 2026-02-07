import threading
import time
import random

def compute_gwa(student_name, grades):
    start_time = time.time()  # start timer

    # simulate different processing times
    time.sleep(random.uniform(0.5, 2))

    gwa = sum(grades) / len(grades)

    end_time = time.time()
    processing_time = end_time - start_time

    print(f"[Thread - {student_name}] "
          f"GWA: {gwa:.2f} | "
          f"Processing Time: {processing_time:.2f} seconds")

# ---- USER INPUT ----
num_students = int(input("Enter number of students: "))

students_data = []

# collect all inputs first
for i in range(num_students):
    student_name = input(f"\nEnter name of student {i+1}: ")

    grades = []
    for j in range(4):
        grade = float(input(f"Enter grade for subject {j+1}: "))
        grades.append(grade)

    students_data.append((student_name, grades))

threads = []

print("\nProcessing...\n")

# start threads AFTER inputs
for student_name, grades in students_data:
    t = threading.Thread(target=compute_gwa, args=(student_name, grades))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\nAll GWA computations completed.")
