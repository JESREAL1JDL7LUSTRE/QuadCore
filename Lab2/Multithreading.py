import time
import threading

def compute_gwa(grades, order):
    print(f"[Thread {order}] Started - Processing grade: {grades[0]}")
    gwa = sum(grades) / len(grades)
    print(f"[Thread {order}] Completed - Grade: {grades[0]}")

InputedGrades = [int(x) for x in input("Enter grade separated by spaces: ").split()]

grades_list = InputedGrades

# Start timing
start_time = time.time()

print("\n" + "="*50)
print("EXECUTION ORDER - THREADING")
print("="*50 + "\n")

threads = []
for i, grade in enumerate(grades_list, 1):
    t = threading.Thread(target=compute_gwa, args=([grade], i))
    threads.append(t)
    t.start()
    print(f"Main: Launched Thread {i}")

for t in threads:
    t.join()

# End timing
end_time = time.time()
execution_time = end_time - start_time

# Calculate final GWA
final_gwa = sum(grades_list) / len(grades_list)

print(f"\n{'='*50}")
print(f"Total threads executed: {len(grades_list)}")
print(f"Final GWA: {final_gwa:.2f}")
print(f"Execution time: {execution_time:.6f} seconds")
print(f"{'='*50}")