Reflection Questions 

1. How did you distribute orders among worker processes? 
The master process (rank 0) generated 5–8 orders and distributed them using a round-robin strategy. Order i was assigned to worker i % num_workers, so orders were spread as evenly as possible. Each worker's batch was sent using comm.send() and received by the worker using comm.recv() via MPI.

2. What happens if there are more orders than workers? 
Round-robin handles this naturally. Extra orders simply wrap back around to earlier workers. For example, with 8 orders and 3 workers, Worker 1 gets 3 orders, Worker 2 gets 3, and Worker 3 gets 2. No order is dropped. If there are fewer orders than workers, some workers receive an empty list and stay idle.

3. How did processing delays affect the order completion? 
Processing delays caused the orders to complete in a non-sequential manner. Even if an order was sent first, it might not finish first because each worker processes tasks independently with different delays. Because each worker used time.sleep() with a random delay between 0.5 and 2.5 seconds, orders did not complete in the same order they were assigned. A worker assigned later could finish before one assigned earlier. This mirrors real-world systems where processing time varies. The master waits for all workers to finish before printing the final list, so the output is always complete regardless of completion order.

4. How did you implement shared memory, and where was it initialized? 
Shared memory was implemented using Manager().list() from Python's multiprocessing module. It was initialized inside the master process (rank 0) after the MPI setup. Workers sent their completed orders back to the master via comm.send(), and the master appended each result to the shared list using a Lock() to prevent conflicts.

5. What issues occurred when multiple workers wrote to shared memory simultaneously? 
Without a lock, a read-modify-write race condition occurred. Two workers would simultaneously read the current list length, get the same index, and then both try to write at that position — causing one worker's order to be overwritten and lost. This was demonstrated in sync_demo.py where 2 out of 8 orders were dropped: NL-1001 and NL-1005 both showed ✗ LOST (race!) in the output.

6. How did you ensure consistent results when using multiple processes? 
A Lock() from Python's multiprocessing module was used. Before appending to the shared list, each process acquires the lock using with lock:, which blocks all other processes from writing until the current one finishes. This guarantees that only one write happens at a time, preventing any data from being lost or overwritten. The result was a consistent and complete list of all 8 orders every time.
