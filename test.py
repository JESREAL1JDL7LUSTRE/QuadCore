import time
import threading

def compute_gwa(student_name, grades):
    """Calculate GWA for a student in a separate thread"""
    print(f"[Thread - {student_name}] Started processing...")
    gwa = sum(grades) / len(grades)
    time.sleep(0.1)  # Simulate some processing time
    print(f"[Thread - {student_name}] Calculated GWA: {gwa:.2f}")
    return gwa

# Input
num_students = int(input("Enter number of students: "))
students = []

# Collect student data
for i in range(1, num_students + 1):
    name = input(f"Enter name of student {i}: ")
    grades = []
    for j in range(1, 5):  # 4 subjects
        grade = int(input(f"Enter grade for subject {j}: "))
        grades.append(grade)
    students.append((name, grades))

# Start timing
start_time = time.time()

print("\n" + "="*50)
print("CALCULATING GWA USING THREADS")
print("="*50 + "\n")

# Create and start threads
threads = []
for student_name, grades in students:
    t = threading.Thread(target=compute_gwa, args=(student_name, grades))
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()

# End timing
end_time = time.time()
execution_time = end_time - start_time

print(f"\n{'='*50}")
print(f"Total students processed: {num_students}")
print(f"Execution time: {execution_time:.6f} seconds")
print(f"{'='*50}")