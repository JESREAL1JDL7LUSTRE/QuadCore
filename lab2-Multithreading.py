import threading

def compute_gwa(grades):
    gwa = sum(grades) / len(grades)
    print(f"[Thread] Calculated GWA: {gwa}")

InputedGrades = [int(x) for x in input("Enter grade separated by spaces: ").split()]

grades_list = InputedGrades

threads = []
for grade in grades_list:
    t = threading.Thread(target=compute_gwa, args=([grade],))
    threads.append(t)
    t.start()

for t in threads:
    t.join()