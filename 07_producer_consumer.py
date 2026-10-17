"""
07_producer_consumer.py
Category: Intermediate / Concurrency & Multithreading

Description:
A multi-threaded Producer-Consumer pipeline:
- Thread-safe bounded `queue.Queue` prevents unbounded memory growth
- Multiple worker consumers executing tasks concurrently
- Graceful shutdown protocol using sentinel "poison pill" markers
- Collects execution statistics (processed count, worker throughput)
"""

import queue
import random
import threading
import time
from typing import List, Dict, Any

POISON_PILL = None  # Sentinel object signaling consumer termination


class Task:
    def __init__(self, task_id: int, payload: str, compute_delay: float):
        self.task_id = task_id
        self.payload = payload
        self.compute_delay = compute_delay

    def __repr__(self):
        return f"<Task id={self.task_id} payload='{self.payload}'>"


class ProducerConsumerPipeline:
    def __init__(self, num_consumers: int = 3, max_queue_size: int = 10):
        self.num_consumers = num_consumers
        self.task_queue: queue.Queue = queue.Queue(maxsize=max_queue_size)
        self.results: List[Dict[str, Any]] = []
        self.results_lock = threading.Lock()
        self.consumers: List[threading.Thread] = []
        self.is_running = False

    def _consumer_worker(self, worker_id: int):
        processed_by_worker = 0
        while True:
            try:
                task = self.task_queue.get(timeout=1.0)
            except queue.Empty:
                continue

            if task is POISON_PILL:
                self.task_queue.task_done()
                break

            # Simulate processing
            time.sleep(task.compute_delay)
            processed_by_worker += 1

            with self.results_lock:
                self.results.append({
                    "task_id": task.task_id,
                    "worker_id": worker_id,
                    "status": "COMPLETED",
                })

            self.task_queue.task_done()

    def start(self):
        self.is_running = True
        for i in range(self.num_consumers):
            thread = threading.Thread(
                target=self._consumer_worker,
                args=(i + 1,),
                name=f"ConsumerWorker-{i + 1}",
                daemon=True,
            )
            self.consumers.append(thread)
            thread.start()

    def submit_task(self, task: Task):
        self.task_queue.put(task)

    def shutdown(self):
        # Wait for all tasks in queue to be processed
        self.task_queue.join()

        # Send termination signal to each consumer
        for _ in range(self.num_consumers):
            self.task_queue.put(POISON_PILL)

        # Wait for all worker threads to exit cleanly
        for thread in self.consumers:
            thread.join()

        self.is_running = False


def main():
    print("=== 07: Producer-Consumer Thread Pool Demo ===")
    pipeline = ProducerConsumerPipeline(num_consumers=3, max_queue_size=5)
    pipeline.start()

    print("Producing 10 tasks to bounded queue...")
    total_tasks = 10
    start_time = time.perf_counter()

    for i in range(1, total_tasks + 1):
        delay = random.uniform(0.02, 0.05)
        task = Task(task_id=i, payload=f"DataChunk_{i}", compute_delay=delay)
        pipeline.submit_task(task)

    print("All tasks submitted. Awaiting processing and shutting down gracefully...")
    pipeline.shutdown()
    elapsed = time.perf_counter() - start_time

    print(f"\nProcessing complete in {elapsed:.3f} seconds.")
    print(f"Total results collected: {len(pipeline.results)}")

    # Distribution by worker
    worker_counts: Dict[int, int] = {}
    for res in pipeline.results:
        w_id = res["worker_id"]
        worker_counts[w_id] = worker_counts.get(w_id, 0) + 1

    print("Task distribution across worker threads:")
    for w_id, count in sorted(worker_counts.items()):
        print(f"  Worker #{w_id}: {count} tasks processed")


if __name__ == "__main__":
    main()
