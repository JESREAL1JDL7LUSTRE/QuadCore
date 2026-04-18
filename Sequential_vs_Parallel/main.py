import random
import time

from sequentialSortingAlgorithm import mergeSort
from parallelSortingAlgorithm import parallelMergeSort
from sequentialSearchingAlgorithm import linearSearch
from parallelSearchingAlgorithm import parallel_linear_search

def generate_data(n):
    return [random.randint(1, 1000000) for _ in range(n)]

def time_function(func, *args):
    start = time.time()
    result = func(*args)
    end = time.time()
    return result, end - start

def run_test(size):
    print("\n" + "=" * 60)
    print(f"DATASET SIZE: {size}")
    print("=" * 60)

    data = generate_data(size)

    target = data[size // 2]

    arr1 = data.copy()
    _, seq_time = time_function(mergeSort, arr1, 0, len(arr1) - 1)

    arr2 = data.copy()
    par_result, par_time = time_function(parallelMergeSort, arr2)

    arr3 = data.copy()
    _, seq_search_time = time_function(linearSearch, arr3, target)

    arr4 = data.copy()
    _, par_search_time = time_function(parallel_linear_search, arr4, target)
