1. Multithreading version:
Takes student names and 4 subject grades per student, creates a thread for each student, each thread calculates the student’s GWA concurrently, and prints the result along with processing time as each thread finishes.

2. Multiprocessing version:
Takes student names and 4 subject grades per student, creates a separate process for each student, each process calculates the student’s GWA independently, and prints the result along with processing time as each process finishes.

3. Execution time for both methods

| Method            | Execution Order| GWA Output| Execution Time |
|-------------------|----------------|-----------|----------------|
| Multithreading    | Data           | Data      | Data           |
| Multiprocessing   | Data           | Data      | Data           |

 bea = 80, 85, 90, 95
 jesreal = 87, 82, 94, 93
 angel = 91, 89, 76, 94
 gil = 98, 90, 88, 95

Discuss why outputs may appear in different order for threads and processes.
Think creatively about how you could optimize your code for faster execution or
better readability.

4. Questions

1. Which approach demonstrates true parallelism in Python? Explain.

2. Compare execution times between multithreading and multiprocessing.

3. Can Python handle true parallelism using threads? Why or why not?

4. What happens if you input a large number of grades (e.g., 1000)? Which
method is faster and why?

5. Which method is better for CPU-bound tasks and which for I/O-bound
tasks?

6. How did your group apply creative coding or algorithmic solutions in this lab?


@JESREAL1JDL7LUSTRE ➜ /workspaces/QuadCore (main) $ python Lab2/Multiprocessing.py
Enter number of students: 4

Enter name of student 1: bea
Enter grade for subject 1: 80
Enter grade for subject 2: 85
Enter grade for subject 3: 90
Enter grade for subject 4: 95

Enter name of student 2: jesreal
Enter grade for subject 1: 87
Enter grade for subject 2: 82
Enter grade for subject 3: 94
Enter grade for subject 4: 93

Enter name of student 3: angel
Enter grade for subject 1: 91
Enter grade for subject 2: 89
Enter grade for subject 3: 76
Enter grade for subject 4: 94

Enter name of student 4: gil
Enter grade for subject 1: 98
Enter grade for subject 2: 90
Enter grade for subject 3: 88
Enter grade for subject 4: 95

==================================================
EXECUTION ORDER - MULTIPROCESSING
==================================================

Main: Launched Process for bea
Main: Launched Process for jesreal
Main: Launched Process for angel
Main: Launched Process for gil
[Process - bea] GWA: 87.50 | Processing Time: 1.05 sec
[Process - jesreal] GWA: 89.00 | Processing Time: 1.22 sec
[Process - angel] GWA: 87.50 | Processing Time: 1.63 sec
[Process - gil] GWA: 92.75 | Processing Time: 1.63 sec

==================================================
Total processes executed: 4
Overall execution time: 1.639969 seconds
==================================================


@JESREAL1JDL7LUSTRE ➜ /workspaces/QuadCore (main) $ python Lab2/Multithreading.py
Enter number of students: 4

Enter name of student 1: bea
Enter grade for subject 1: 80
Enter grade for subject 2: 85
Enter grade for subject 3: 90
Enter grade for subject 4: 95

Enter name of student 2: jesreal
Enter grade for subject 1: 87
Enter grade for subject 2: 82
Enter grade for subject 3: 94
Enter grade for subject 4: 93

Enter name of student 3: angel
Enter grade for subject 1: 91
Enter grade for subject 2: 89
Enter grade for subject 3: 76
Enter grade for subject 4: 94

Enter name of student 4: gil
Enter grade for subject 1: 98
Enter grade for subject 2: 90
Enter grade for subject 3: 88
Enter grade for subject 4: 95

==================================================
EXECUTION ORDER - MULTITHREADING
==================================================

Main: Launched Thread for bea
Main: Launched Thread for jesreal
Main: Launched Thread for angel
Main: Launched Thread for gil
[Thread - angel] GWA: 87.50 | Processing Time: 0.78 sec
[Thread - gil] GWA: 92.75 | Processing Time: 1.18 sec
[Thread - jesreal] GWA: 89.00 | Processing Time: 1.77 sec
[Thread - bea] GWA: 87.50 | Processing Time: 1.97 sec

==================================================
Total threads executed: 4
Overall execution time: 1.973820 seconds
==================================================
@JESREAL1JDL7LUSTRE ➜ /workspaces/QuadCore (main) $ 