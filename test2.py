import time
import threading
from queue import Queue

def compute_gwa(subject_name, grade, order, results_queue):
    """
    Compute GWA for a single subject grade
    Args:
        subject_name: Name of the subject
        grade: Numerical grade for the subject
        order: Thread execution order
        results_queue: Thread-safe queue to store results
    """
    thread_id = threading.get_ident()
    print(f"[Thread {order}] (ID: {thread_id}) Started - Processing {subject_name}: {grade}")
    
    # Simulate some processing time
    time.sleep(0.1)
    
    # Store result in thread-safe queue
    results_queue.put({
        'subject': subject_name,
        'grade': grade,
        'order': order
    })
    
    print(f"[Thread {order}] (ID: {thread_id}) Completed - {subject_name}: {grade}")

def get_subject_input():
    """Get subject names and grades from user"""
    print("="*60)
    print("GRADE CALCULATOR - MULTITHREADING MODE")
    print("="*60)
    
    subjects = []
    grades = []
    
    num_subjects = int(input("\nEnter number of subjects: "))
    
    for i in range(num_subjects):
        subject = input(f"Enter subject {i+1} name: ").strip()
        grade = float(input(f"Enter grade for {subject}: "))
        subjects.append(subject)
        grades.append(grade)
    
    return subjects, grades

# Get input from user
subjects, grades_list = get_subject_input()

# Create thread-safe queue for results
results_queue = Queue()

# Start timing
start_time = time.time()

print("\n" + "="*60)
print("EXECUTION ORDER - MULTITHREADING")
print("="*60 + "\n")

threads = []
for i, (subject, grade) in enumerate(zip(subjects, grades_list), 1):
    t = threading.Thread(target=compute_gwa, args=(subject, grade, i, results_queue))
    threads.append(t)
    t.start()
    print(f"Main: Launched Thread {i} for {subject}")

# Wait for all threads to complete
for t in threads:
    t.join()

# End timing
end_time = time.time()
execution_time = end_time - start_time

# Collect results from queue
results = []
while not results_queue.empty():
    results.append(results_queue.get())

# Sort results by order
results.sort(key=lambda x: x['order'])

# Calculate final GWA
final_gwa = sum(grades_list) / len(grades_list)

# Display results
print(f"\n{'='*60}")
print("GRADE SUMMARY")
print(f"{'='*60}")
for result in results:
    print(f"{result['subject']:<20} : {result['grade']:.2f}")

print(f"\n{'='*60}")
print(f"Total threads executed: {len(grades_list)}")
print(f"Final GWA: {final_gwa:.2f}")
print(f"Execution time: {execution_time:.6f} seconds")
print(f"Processing method: MULTITHREADING")
print(f"{'='*60}")