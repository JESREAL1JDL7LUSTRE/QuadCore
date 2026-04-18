#Parallel Merge Sort Algorithm

from multiprocessing import Process, Queue
from sequentialSortingAlgorithm import mergeSort

def mergeTwo(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

def worker(chunk, q):
    q.put(mergeSort(chunk, 0, len(chunk) - 1))

def parallelMergeSort(arr, numProcesses=4):
    if len(arr) <= 1:
        return arr

    numProcesses = min(numProcesses, len(arr))
    size = len(arr) // numProcesses

    chunks = [arr[i * size:(i + 1) * size] for i in range(numProcesses - 1)]
    chunks.append(arr[(numProcesses - 1) * size:])

    q = Queue()
    processes = []

    for chunk in chunks:
        p = Process(target=worker, args=(chunk, q))
        processes.append(p)
        p.start()

    sortedChunks = [q.get() for _ in processes]

    for p in processes:
        p.join()

    result = sortedChunks[0]
    for i in range(1, len(sortedChunks)):
        result = mergeTwo(result, sortedChunks[i])

    return result