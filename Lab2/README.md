1. Multithreading version:
Takes student names and 4 subject grades per student, creates a thread for each student, each thread calculates the student’s GWA concurrently, and prints the result along with processing time as each thread finishes.

2. Multiprocessing version:
Takes student names and 4 subject grades per student, creates a separate process for each student, each process calculates the student’s GWA independently, and prints the result along with processing time as each process finishes.

3. Execution time for both methods

| Method            |      Execution Order       |         GWA Output         | Execution Time |
|-------------------|----------------------------|----------------------------|----------------|
| Multithreading    | a, g, j, b = Concurrency   | 87.50, 92.75, 89.00, 87.50 | 1.973820 secs  |
| Multiprocessing   | b, j, a, g = Independently | 87.50, 89.00, 87.50, 92.75 | 1.639969 secs  |

Sample Inputs:
 bea = 80, 85, 90, 95       (b)
 jesreal = 87, 82, 94, 93   (j)
 angel = 91, 89, 76, 94     (a)
 gil = 98, 90, 88, 95       (g)

Discuss why outputs may appear in different order for threads and processes.
Think creatively about how you could optimize your code for faster execution or
better readability.

When you run multiple threads or processes, the output order can vary each time because the operating system decides which one runs when based on CPU availability, system load, and other factors, so tasks that start in one order may finish in another.

There are several ways on how we can optimize our code for faster execution and better readability. First, we must choose either multiprocessing or multithreading based on its usage. In multithreading, threads share memory and switch rapidly, so whichever thread reaches the print statement first shows up in the output. Python's Global Interpreter Lock (GIL) adds another layer of timing complexity here. With multiprocessing, each process has its own memory and can run truly in parallel on different CPU cores, so they finish independently and results appear in whatever order they complete.

The readability of the code can be improved by organizing it into clear functions, which makes it easier to read, maintain, and modify. Use multithreading for I/O tasks like reading files or making network requests, and multiprocessing for heavy computation like math or data processing. Make your code readable by breaking it into clear functions and using list comprehensions where appropriate. Consistent output formatting also helps, especially when multiple things are running at once.


Why outputs may appear in different order

Multithreading (Concurrency / Interleaved Execution)

Threads share the same memory and are controlled by Python’s Global Interpreter Lock (GIL).

The GIL allows only one thread to execute Python code at a time, so the threads take turns running.

Because of this rapid switching and the random delays we added, threads may finish in a different order than the order they were started.

That’s why the GWA outputs for Bea, Jesreal, Angel, and Gil appear in the order a, g, j, b instead of the input order.

Multiprocessing (Independent Execution / True Parallelism)

Each process runs independently in its own memory space and can run on a separate CPU core.

Processes don’t share memory, so they can truly run at the same time.

The completion order depends on processing time and random delays, not the order the processes were launched.

That’s why the outputs appear in a different order (b, j, a, g) than the input order.
4. Questions

1. Which approach demonstrates true parallelism in Python? Explain.
- Multiprocessing demonstrates true parallelism in Python. This is because each process runs independently on its own CPU core with its own memory space, so multiple processes can actually execute at the same time. Threads, on the other hand, share the same memory and are limited by Python’s Global Interpreter Lock (GIL), which means only one thread can do CPU work at a time. That’s why threads run concurrently but don’t achieve real parallelism.

2. Compare execution times between multithreading and multiprocessing.
- In the experiment, multiprocessing completed faster than multithreading, with an overall execution time of approximately 1.64 seconds compared to 1.97 seconds for multithreading. This difference occurred because multiprocessing allowed tasks to execute independently without Global Interpreter Lock interference, while multithreading incurred additional overhead from context switching and lock management.

3. Can Python handle true parallelism using threads? Why or why not?
- No, Python cannot achieve true parallelism with threads for CPU-heavy tasks because of the Global Interpreter Lock (GIL). The GIL ensures that only one thread executes Python code at a time, so even if you create multiple threads, they take turns running. Threads can still run concurrently when waiting for I/O operations, but for computations like calculating GWA, they do not run at the same time. To achieve true parallelism, you need multiprocessing, where each process runs independently on its own CPU core.

4. What happens if you input a large number of grades (e.g., 1000)? Which method is faster and why?
- Multithreading would likely be "faster" in terms of system stability, but not calculation speed. Creating 1,000 threads is relatively easy for most modern OS. While, Multiprocessing would be significantly faster at the math, but launching 1,000 separate processes might crash your RAM or cause the OS to "thrash" as it struggles to manage 1,000 separate memory allocations.

5. Which method is better for CPU-bound tasks and which for I/O-bound
tasks?
- Multiprocessing is better for CPU-bound tasks because it bypasses the Global Interpreter Lock and utilizes multiple cores for parallel computation. Multithreading is better for I/O-bound tasks since threads release the Global Interpreter Lock during I/O operations, allowing efficient overlap of waiting times with execution.

6. How did your group apply creative coding or algorithmic solutions in this lab?
- In this lab, we used multithreading and multiprocessing to compute student GWAs, and added processing time tracking and random delays. The delays were included to simulate different workloads so we could clearly see how threads and processes run at the same time and observe the order in which they finish. This helped us better understand concurrency and parallelism in Python. 


SAMPLE EXECUTIONS:

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