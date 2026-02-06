import time
from multiprocessing import Process

def compute_gwa_mp(grades):
    gwa = sum(grades) / len(grades)
    print(f"[Process] Calculated GWA: {gwa}")

InputedGrades = [int(x) for x in input("Enter grade separated by spaces: ").split()]

grades_list = InputedGrades

# Start timing
start_time = time.time()

processes = []
for grade in grades_list:
    p = Process(target=compute_gwa_mp, args=([grade],))
    processes.append(p)
    p.start()

for p in processes:
    p.join()

# End timing
end_time = time.time()
execution_time = end_time - start_time

print(f"\nExecution time: {execution_time:.6f} seconds")