import time
import threading

def compute_gwa(grades):
    gwa = sum(grades) / len(grades)
    print(f"[Thread] Calculated GWA: {gwa}")

InputedGrades = [int(x) for x in input("Enter grade separated by spaces: ").split()]

grades_list = InputedGrades

# Start timing
start_time = time.time()

threads = []
for grade in grades_list:
    t = threading.Thread(target=compute_gwa, args=([grade],))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# End timing
end_time = time.time()
execution_time = end_time - start_time

print(f"\nExecution time: {execution_time:.6f} seconds")