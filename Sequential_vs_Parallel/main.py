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
