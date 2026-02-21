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
