"""
Laundry Pipeline Parallel Processing Simulation
================================================
Pipeline logic:
  Load 1: SORT → WASH → DRY → FOLD
  Load 2:      SORT → WASH → DRY → FOLD
  Load 3:           SORT → WASH → DRY → FOLD

While Load 1 is DRYING, Load 2 is WASHING, Load 3 is SORTING.
One washer (sequential), one dryer (sequential), but they run simultaneously
because they are DIFFERENT machines serving different loads at the same time.
"""

import time
import threading
from concurrent.futures import ThreadPoolExecutor

# ── Simulated durations ────────────────────────────────────────────────────────
SORT_TIME        = 0.5
WASH_TIME        = 1.0
DRY_TIME         = 1.5
FOLD_TIME        = 0.75
NUM_LOADS        = 6
NUM_FOLD_WORKERS = 3

# ── Shared appliances: only 1 load uses each at a time ────────────────────────
# (but washer and dryer can run SIMULTANEOUSLY with different loads)
washer_semaphore = threading.Semaphore(1)
dryer_semaphore  = threading.Semaphore(1)

# ── Shared output log (requires mutex to avoid race conditions) ────────────────
folded_log = []
log_lock   = threading.Lock()

# ── Stage functions ────────────────────────────────────────────────────────────
def sort_load(load_id):
    print(f"  [SORT ] Load {load_id} sorting...")
    time.sleep(SORT_TIME)

def wash_load(load_id):
    print(f"  [WASH ] Load {load_id} washing...")
    time.sleep(WASH_TIME)

def dry_load(load_id):
    print(f"  [DRY  ] Load {load_id} drying...")
    time.sleep(DRY_TIME)

def fold_portion(load_id, portion):
    time.sleep(FOLD_TIME / NUM_FOLD_WORKERS)
    return portion

# ══════════════════════════════════════════════════════════════════════════════
# SEQUENTIAL VERSION
# ══════════════════════════════════════════════════════════════════════════════
def sequential():
    """One person, one load at a time, all stages before moving on."""
    print("\n[SEQUENTIAL] Starting...")
    start = time.perf_counter()

    for load_id in range(1, NUM_LOADS + 1):
        sort_load(load_id)
        wash_load(load_id)
        dry_load(load_id)
        for portion in range(NUM_FOLD_WORKERS):
            fold_portion(load_id, portion)
        print(f"  [DONE ] Load {load_id} complete.\n")

    elapsed = time.perf_counter() - start
    print(f"[SEQUENTIAL] Total time: {elapsed:.2f}s")
    return elapsed

# ══════════════════════════════════════════════════════════════════════════════
# PARALLEL VERSION — Pipelined
# ══════════════════════════════════════════════════════════════════════════════
def parallel():
    """
    Each load runs as its own thread.

    The pipeline works like this:
      Load 1 finishes SORT → grabs washer → starts WASH
      Load 2 finishes SORT → waits for washer (Load 1 using it)
      Load 1 finishes WASH → releases washer → grabs dryer → starts DRY
      Load 2 gets washer  → starts WASH   ← washer AND dryer both busy!
      Load 3 finishes SORT → waits for washer
      Load 1 finishes DRY → releases dryer → starts FOLD
      Load 2 finishes WASH → releases washer → grabs dryer → starts DRY
      Load 3 gets washer  → starts WASH   ← all 3 machines overlapping!
      ...and so on
    """
    print("\n[PARALLEL] Starting (pipeline)...")
    start = time.perf_counter()

    # Stagger sort starts so loads enter the pipeline one at a time
    sort_events = [threading.Event() for _ in range(NUM_LOADS)]

    def pipeline_load(i):
        load_id = i + 1

        # SORT — wait for previous load to finish sorting first
        if i > 0:
            sort_events[i - 1].wait()
        sort_load(load_id)
        sort_events[i].set()   # signal next load: you can sort now

        # WASH — acquire washer, then release it before moving to dryer
        with washer_semaphore:
            wash_load(load_id)
        # washer is released HERE → next load starts washing
        # while THIS load moves on to grab the dryer

        # DRY — acquire dryer independently (different machine from washer)
        with dryer_semaphore:
            dry_load(load_id)
        # dryer released HERE → next load starts drying
        # while THIS load moves on to fold

        # FOLD — data parallelism: 3 threads fold portions simultaneously
        with ThreadPoolExecutor(max_workers=NUM_FOLD_WORKERS) as fold_pool:
            futures = [
                fold_pool.submit(fold_portion, load_id, p)
                for p in range(NUM_FOLD_WORKERS)
            ]
            for f in futures:
                f.result()

        # Write to shared log — mutex prevents race conditions
        with log_lock:
            folded_log.append(f"Load {load_id} complete.")
            print(f"  [DONE ] Load {load_id} complete.\n")

    # Launch all load threads concurrently (task parallelism)
    with ThreadPoolExecutor(max_workers=NUM_LOADS) as pool:
        futures = [pool.submit(pipeline_load, i) for i in range(NUM_LOADS)]
        for f in futures:
            f.result()

    elapsed = time.perf_counter() - start
    print(f"[PARALLEL] Total time: {elapsed:.2f}s")
    return elapsed

# ══════════════════════════════════════════════════════════════════════════════
# BENCHMARK
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 55)
    print("  LAUNDRY PIPELINE BENCHMARK")
    print(f"  Loads: {NUM_LOADS}  |  Fold Workers: {NUM_FOLD_WORKERS}")
    print("=" * 55)

    seq_time = sequential()

    folded_log.clear()
    par_time = parallel()

    speedup    = seq_time / par_time
    ideal      = NUM_LOADS
    efficiency = (speedup / ideal) * 100

    print("\n" + "=" * 55)
    print("  BENCHMARK RESULTS")
    print("=" * 55)
    print(f"  Sequential time : {seq_time:.2f}s")
    print(f"  Parallel time   : {par_time:.2f}s")
    print(f"  Speedup         : {speedup:.2f}x")
    print(f"  Ideal speedup   : ~{ideal}x (linear)")
    print(f"  Efficiency      : {efficiency:.1f}%")
    print("=" * 55)
    print(f"\n  Folded log: {folded_log}")