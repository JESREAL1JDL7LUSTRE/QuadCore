import time
from multiprocessing import Process

def compute_gwa_mp(grades, order):
    print(f"[Process {order}] Started - Processing grade: {grades[0]}")
    gwa = sum(grades) / len(grades)
    print(f"[Process {order}] Completed - Grade: {grades[0]}")

InputedGrades = [int(x) for x in input("Enter grade separated by spaces: ").split()]

grades_list = InputedGrades

# Start timing
start_time = time.time()

print("\n" + "="*50)
print("EXECUTION ORDER - MULTIPROCESSING")
print("="*50 + "\n")

processes = []
for i, grade in enumerate(grades_list, 1):
    p = Process(target=compute_gwa_mp, args=([grade], i))
    processes.append(p)
    p.start()
    print(f"Main: Launched Process {i}")

for p in processes:
    p.join()

# End timing
end_time = time.time()
execution_time = end_time - start_time

# Calculate final GWA
final_gwa = sum(grades_list) / len(grades_list)

print(f"\n{'='*50}")
print(f"Total processes executed: {len(grades_list)}")
print(f"Final GWA: {final_gwa:.2f}")
print(f"Execution time: {execution_time:.6f} seconds")
print(f"{'='*50}")