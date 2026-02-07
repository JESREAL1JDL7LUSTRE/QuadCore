import time
import random
from multiprocessing import Process

def compute_gwa_mp(student_name, grades):
    start_time = time.time()

    # simulate variable processing times to observe order
    time.sleep(random.uniform(0.5, 2))

    gwa = sum(grades) / len(grades)
    processing_time = time.time() - start_time

    print(f"[Process - {student_name}] GWA: {gwa:.2f} | Processing Time: {processing_time:.2f} sec")

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

processes = []

print("\n" + "="*50)
print("EXECUTION ORDER - MULTIPROCESSING")
print("="*50 + "\n")

start_time = time.time()

# start a process for each student
for student_name, grades in students_data:
    p = Process(target=compute_gwa_mp, args=(student_name, grades))
    processes.append(p)
    p.start()
    print(f"Main: Launched Process for {student_name}")

# wait for all processes to finish
for p in processes:
    p.join()

end_time = time.time()
execution_time = end_time - start_time

print(f"\n{'='*50}")
print(f"Total processes executed: {len(students_data)}")
print(f"Overall execution time: {execution_time:.6f} seconds")
print(f"{'='*50}")
