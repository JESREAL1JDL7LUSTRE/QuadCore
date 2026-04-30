from multiprocessing import Manager, Lock, Process
import time
import random

def worker_no_lock(worker_id: int, orders: list, shared: list, counter: list):
    for order in orders:
        delay = random.uniform(0.05, 0.15)
        time.sleep(delay)

        # Unsafe: read index, sleep, then write — other worker may grab same idx
        idx = len(shared)
        time.sleep(0.05)
        if idx == len(shared):
            shared.append({**order, "worker": worker_id})
            print(f"  [W{worker_id}-NoLock] Stored {order['order_id']}")
        else:
            print(f"  [W{worker_id}-NoLock] ✗ LOST {order['order_id']} (race!)")
            counter[0] += 1


def worker_with_lock(worker_id: int, orders: list, shared: list, lock: Lock):
    for order in orders:
        delay = random.uniform(0.05, 0.15)
        time.sleep(delay)
        with lock:
            shared.append({**order, "worker": worker_id})
        print(f"  [W{worker_id}-Lock]   Stored {order['order_id']}")


def make_orders(prefix: str):
    items = ["Laptop", "Keyboard", "Monitor", "Headset", "Webcam", "Mouse", "USB Hub", "SSD Drive"]
    all_orders = [{"order_id": f"{prefix}-{1000+i}", "item": items[i % len(items)]} for i in range(8)]
    return all_orders[:4], all_orders[4:]


def section(title: str):
    print("\n" + "=" * 55)
    print(f"  {title}")
    print("=" * 55)


def demo_without_lock():
    section("DEMO 1 – NO LOCK (race conditions cause data loss)")
    manager = Manager()
    shared  = manager.list()
    counter = manager.list([0])

    batch_a, batch_b = make_orders("NL")
    p1 = Process(target=worker_no_lock, args=(1, batch_a, shared, counter))
    p2 = Process(target=worker_no_lock, args=(2, batch_b, shared, counter))
    p1.start(); p2.start()
    p1.join();  p2.join()

    stored = len(shared)
    lost   = counter[0]
    print(f"\n  Expected 8 orders — got {stored} stored, {lost} lost.")
    if lost > 0:
        print("  ⚠  Race condition detected: orders were dropped!")
    else:
        print("  (No loss this run — races are non-deterministic, try again.)")
    return stored, lost


def demo_with_lock():
    section("DEMO 2 – WITH LOCK (all orders safely preserved)")
    manager = Manager()
    shared  = manager.list()
    lock    = Lock()

    batch_a, batch_b = make_orders("LK")
    p1 = Process(target=worker_with_lock, args=(1, batch_a, shared, lock))
    p2 = Process(target=worker_with_lock, args=(2, batch_b, shared, lock))
    p1.start(); p2.start()
    p1.join();  p2.join()

    stored = len(shared)
    print(f"\n  Expected 8 orders — got {stored}.")
    if stored == 8:
        print("  ✓ All orders stored correctly!")
    return stored


if __name__ == "__main__":
    stored_no_lock, lost = demo_without_lock()
    stored_with_lock     = demo_with_lock()

    section("SUMMARY")
    print(f"  Without lock : {stored_no_lock}/8 stored  |  {lost} order(s) lost")
    print(f"  With lock    : {stored_with_lock}/8 stored  |  0 order(s) lost")
    print()