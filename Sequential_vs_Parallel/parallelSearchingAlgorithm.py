# Parallel Linear Search Algorithm

from multiprocessing import Process, Queue

def worker(sub_arr, x, q, offset):
    for i in range(len(sub_arr)):
        if sub_arr[i] == x:
            q.put(offset + i)
            return
    q.put(-1)

def parallel_linear_search(arr, x, num_processes=4):
    if len(arr) == 0:
        return -1

    num_processes = min(num_processes, len(arr))
    size = len(arr) // num_processes

    chunks = [arr[i * size:(i + 1) * size] for i in range(num_processes - 1)]
    chunks.append(arr[(num_processes - 1) * size:])

    q = Queue()
    processes = []

    start = 0
    for chunk in chunks:
        p = Process(target=worker, args=(chunk, x, q, start))
        processes.append(p)
        p.start()
        start += len(chunk)

    results = [q.get() for _ in processes]

    for p in processes:
        p.join()

    valid_results = [index for index in results if index != -1]

    if valid_results:
        return min(valid_results)
    return -1