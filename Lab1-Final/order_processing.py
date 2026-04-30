from mpi4py import MPI
from multiprocessing import Manager, Lock
import time
import random

ITEMS = [
    "Laptop", "Keyboard", "Monitor", "Headset", "Webcam",
    "Mouse", "USB Hub", "SSD Drive", "GPU Card", "RAM Module",
]

def generate_orders(count):
    return [
        {"order_id": f"ORD-{1000 + i}", "item": random.choice(ITEMS)}
        for i in range(count)
    ]

def distribute_orders(orders, num_workers):
    buckets = [[] for _ in range(num_workers)]
    for i, order in enumerate(orders):
        buckets[i % num_workers].append(order)
    return buckets

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if size < 2:
        if rank == 0:
            print("[ERROR] Please run with at least 2 processes.")
            print("        Example: mpirun --oversubscribe -np 4 python order_processing.py")
        return

    num_workers = size - 1

    # MASTER (rank 0)
    if rank == 0:
        # Shared memory lives here in the master
        manager = Manager()
        shared_orders = manager.list()
        lock = Lock()

        num_orders = random.randint(5, 8)
        orders = generate_orders(num_orders)

        print("\n" + "=" * 55)
        print("  DISTRIBUTED ORDER PROCESSING SYSTEM  ")
        print("=" * 55)
        print(f"\n[Master] Generated {num_orders} orders:")
        for o in orders:
            print(f"         {o['order_id']} → {o['item']}")

        buckets = distribute_orders(orders, num_workers)

        for worker_rank in range(1, size):
            batch = buckets[worker_rank - 1]
            comm.send(batch, dest=worker_rank, tag=10)
            print(f"\n[Master] Sent {len(batch)} order(s) to Worker {worker_rank}")

        # Collect results from each worker via MPI
        for worker_rank in range(1, size):
            results = comm.recv(source=worker_rank, tag=20)
            print(f"[Master] Worker {worker_rank} finished — received {len(results)} result(s).")
            with lock:
                for r in results:
                    shared_orders.append(r)

        # Print final results from shared memory
        print("\n" + "=" * 55)
        print("  FINAL PROCESSED ORDERS (from shared memory)  ")
        print("=" * 55)
        for entry in sorted(shared_orders, key=lambda x: x["order_id"]):
            print(f"  {entry['order_id']} | {entry['item']:<14} | "
                  f"Worker {entry['worker']} | {entry['duration']:.2f}s")
        print(f"\n[Master] Total orders completed: {len(shared_orders)}/{num_orders}")
        print("=" * 55 + "\n")

    # WORKERS (rank 1 … N-1)
    else:
        assigned = comm.recv(source=0, tag=10)

        if not assigned:
            print(f"[Worker {rank}] No orders assigned. Idle.")
            comm.send([], dest=0, tag=20)
            return

        print(f"\n[Worker {rank}] Received {len(assigned)} order(s): "
              f"{[o['order_id'] for o in assigned]}")

        completed = []
        for order in assigned:
            delay = round(random.uniform(0.5, 2.5), 2)
            print(f"  [Worker {rank}] Processing {order['order_id']} "
                  f"({order['item']}) … sleeping {delay}s")
            time.sleep(delay)
            completed.append({
                "order_id": order["order_id"],
                "item":     order["item"],
                "worker":   rank,
                "duration": delay,
            })
            print(f"  [Worker {rank}] ✓ Completed {order['order_id']}")

        # Send all results back to master
        comm.send(completed, dest=0, tag=20)

if __name__ == "__main__":
    main()