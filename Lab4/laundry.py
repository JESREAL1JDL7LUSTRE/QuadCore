"""
Laundry Parallel Processing Simulation
=======================================
Real-world bottleneck: A single person sequentially handling all laundry
tasks (sort → wash → dry → fold) for multiple loads, one load at a time.

Sequential model: Each load must finish all 4 stages before the next begins.
Parallel model:   Multiple loads are pipelined using task parallelism —
                  while Load N is drying, Load N-1 is being folded and
                  Load N+1 is being washed, etc. Data parallelism is also
                  applied within folding (multiple workers fold simultaneously).
"""

import time
import threading
import random
from concurrent.futures import ThreadPoolExecutor

# ─────────────────────────────────────────────
# Simulated task durations (seconds, scaled)
# Real-world: sort≈5min, wash≈30min, dry≈45min, fold≈15min
# Simulated at 1:60 ratio → 0.08, 0.5, 0.75, 0.25 sec per load
# ─────────────────────────────────────────────
SORT_TIME  = 0.08   # seconds
WASH_TIME  = 0.50
DRY_TIME   = 0.75
FOLD_TIME  = 0.25

NUM_LOADS  = 6      # total loads of laundry
NUM_FOLD_WORKERS = 3  # parallel folding threads (data parallelism)

lock = threading.Lock()

def sort_load(load_id):
    time.sleep(SORT_TIME)
    return load_id

def wash_load(load_id):
    time.sleep(WASH_TIME)
    return load_id

def dry_load(load_id):
    time.sleep(DRY_TIME)
    return load_id

def fold_portion(load_id, portion):
    """Fold one portion of a load (data parallelism within folding)."""
    time.sleep(FOLD_TIME / NUM_FOLD_WORKERS)
    return portion

# ─────────────────────────────────────────────
# SEQUENTIAL VERSION
# ─────────────────────────────────────────────
def sequential():
    """
    One person handles each load completely (sort→wash→dry→fold)
    before moving to the next load.
    """
    print("\n[SEQUENTIAL] Starting...")
    start = time.perf_counter()

    for load_id in range(1, NUM_LOADS + 1):
        sort_load(load_id)
        wash_load(load_id)
        dry_load(load_id)
        # Folding is also done sequentially, one item at a time
        for portion in range(NUM_FOLD_WORKERS):
            fold_portion(load_id, portion)
        print(f"  Load {load_id} complete.")

    elapsed = time.perf_counter() - start
    print(f"[SEQUENTIAL] Total time: {elapsed:.4f}s")
    return elapsed

# ─────────────────────────────────────────────
# PARALLEL VERSION — Pipelined Task Parallelism
# + Data Parallelism within Folding
# ─────────────────────────────────────────────
def parallel():
    """
    Task parallelism: overlapping pipeline stages across loads.
      - Sort stage runs ahead while earlier loads wash/dry/fold.
    Data parallelism: folding is split across multiple threads simultaneously.

    Implementation uses a semaphore-gated pipeline with a thread pool.
    """
    print("\n[PARALLEL] Starting...")
    start = time.perf_counter()

    # Shared pipeline queues (simulated via events for each load)
    sorted_events  = [threading.Event() for _ in range(NUM_LOADS)]
    washed_events  = [threading.Event() for _ in range(NUM_LOADS)]
    dried_events   = [threading.Event() for _ in range(NUM_LOADS)]
    folded_events  = [threading.Event() for _ in range(NUM_LOADS)]

    def pipeline_load(i):
        """Each load goes through its stages, but stages overlap across loads."""
        load_id = i + 1

        # SORT (can start as soon as previous sort is done — sequential gate)
        if i > 0:
            sorted_events[i - 1].wait()  # wait for previous load to be sorted
        sort_load(load_id)
        sorted_events[i].set()

        # WASH (can start immediately after sort; machine handles it)
        wash_load(load_id)
        washed_events[i].set()

        # DRY (starts right after wash; dryer handles it)
        dry_load(load_id)
        dried_events[i].set()

        # FOLD — Data Parallelism: split folding across worker threads
        with ThreadPoolExecutor(max_workers=NUM_FOLD_WORKERS) as fold_pool:
            futures = [
                fold_pool.submit(fold_portion, load_id, p)
                for p in range(NUM_FOLD_WORKERS)
            ]
            for f in futures:
                f.result()  # wait for all fold workers
        folded_events[i].set()

        with lock:
            print(f"  Load {load_id} complete.")

    # Launch all load pipelines concurrently (task parallelism)
    with ThreadPoolExecutor(max_workers=NUM_LOADS) as pool:
        futures = [pool.submit(pipeline_load, i) for i in range(NUM_LOADS)]
        for f in futures:
            f.result()

    elapsed = time.perf_counter() - start
    print(f"[PARALLEL] Total time: {elapsed:.4f}s")
    return elapsed

# ─────────────────────────────────────────────
# BENCHMARK
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  LAUNDRY PARALLEL PROCESSING BENCHMARK")
    print(f"  Loads: {NUM_LOADS}  |  Fold Workers: {NUM_FOLD_WORKERS}")
    print("=" * 55)

    # Warm-up (eliminate cold-start variance)
    for _ in range(2):
        sort_load(0); wash_load(0); dry_load(0)

    seq_time  = sequential()
    par_time  = parallel()
    speedup   = seq_time / par_time
    ideal     = NUM_LOADS  # ideal linear speedup

    print("\n" + "=" * 55)
    print("  BENCHMARK RESULTS")
    print("=" * 55)
    print(f"  Sequential time : {seq_time:.4f} seconds")
    print(f"  Parallel time   : {par_time:.4f} seconds")
    print(f"  Speedup         : {speedup:.2f}x")
    print(f"  Ideal speedup   : ~{ideal}x (linear)")
    efficiency = (speedup / ideal) * 100
    print(f"  Efficiency      : {efficiency:.1f}%")
    print("=" * 55)

    print("\n  ANALYSIS:")
    if speedup >= ideal * 0.7:
        print("  Good speedup — pipeline effectively overlaps stages.")
    else:
        print("  Speedup below ideal — bottlenecks present:")
        print("  - Sort stage is serialized (one sorter, sequential gate).")
        print("  - Thread overhead from frequent context switches.")
        print("  - Dry time dominates; earlier stages wait on dryer.")
    print()