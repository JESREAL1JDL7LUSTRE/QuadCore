import threading
import time
import random

def compute_gwa(student_name, grades):
    start_time = time.time()

    # simulate variable processing times
    time.sleep(random.uniform(0.5, 2))

    gwa = sum(grades) / len(grades)
    processing_time = time.time() - start_time

    print(f"[Thread - {student_name}] GWA: {gwa:.2f} | Processing Time: {processing_time:.2f} sec")

# ---- USER INPUT ----
num_students = int(input("Enter number of students: "))
students_data = []

for i in range(num_students):
    student_name = input(f"\nEnter name of student {i+1}: ")
    grades = []
    for j in range(4):
        grade = float(input(f"Enter grade for subject {j+1}: "))
        grades.append(grade)
    students_data.append((student_name, grades))

threads = []

print("\n" + "="*50)
print("EXECUTION ORDER - MULTITHREADING")
print("="*50 + "\n")

start_time = time.time()

# start a thread for each student
for student_name, grades in students_data:
    t = threading.Thread(target=compute_gwa, args=(student_name, grades))
    threads.append(t)
    t.start()
    print(f"Main: Launched Thread for {student_name}")

# wait for all threads to finish
for t in threads:
    t.join()

end_time = time.time()
execution_time = end_time - start_time

print(f"\n{'='*50}")
print(f"Total threads executed: {len(students_data)}")
print(f"Overall execution time: {execution_time:.6f} seconds")
print(f"{'='*50}")
