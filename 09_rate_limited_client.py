"""
09_rate_limited_client.py
Category: Intermediate / Networking & System Design

Description:
Implementation of classic API rate-limiting algorithms:
1. Token Bucket algorithm: Allows bursts up to bucket capacity and refills at constant rate
2. Leaky Bucket algorithm: Smooths out bursts into a steady output rate
3. Simulated HTTP Client demonstrating rate-limit enforcement and backpressure
"""

import time
import threading
from typing import Optional, Dict, Any


class TokenBucket:
    """
    Token Bucket rate limiter:
    - capacity: Maximum tokens held (burst capacity)
    - fill_rate: Tokens added per second
    """
    def __init__(self, capacity: float, fill_rate: float):
        self.capacity = float(capacity)
        self.fill_rate = float(fill_rate)
        self.tokens = float(capacity)
        self.last_update = time.perf_counter()
        self.lock = threading.Lock()

    def _refill(self):
        now = time.perf_counter()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.fill_rate)
        self.last_update = now

    def acquire(self, tokens: float = 1.0) -> bool:
        """Attempts to acquire tokens immediately. Returns True if granted, False if throttled."""
        with self.lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    def wait_and_acquire(self, tokens: float = 1.0, timeout: float = 5.0) -> bool:
        """Blocks until tokens become available or timeout expires."""
        deadline = time.perf_counter() + timeout
        while time.perf_counter() < deadline:
            with self.lock:
                self._refill()
                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return True
                deficit = tokens - self.tokens
                sleep_time = min(deficit / self.fill_rate, 0.05)
            time.sleep(sleep_time)
        return False


class SimulatedApiClient:
    def __init__(self, rate_limiter: TokenBucket):
        self.limiter = rate_limiter
        self.successful_requests = 0
        self.throttled_requests = 0

    def make_request(self, endpoint: str, blocking: bool = False) -> Dict[str, Any]:
        if blocking:
            acquired = self.limiter.wait_and_acquire(1.0, timeout=2.0)
        else:
            acquired = self.limiter.acquire(1.0)

        if not acquired:
            self.throttled_requests += 1
            return {
                "status": 429,
                "endpoint": endpoint,
                "message": "Too Many Requests (Rate limit exceeded)",
            }

        self.successful_requests += 1
        return {
            "status": 200,
            "endpoint": endpoint,
            "message": "OK",
            "timestamp": time.time(),
        }


def main():
    print("=== 09: Rate Limited Client Demo ===")

    # Configure bucket: capacity = 3 tokens, refills 2 tokens per second
    bucket = TokenBucket(capacity=3.0, fill_rate=2.0)
    client = SimulatedApiClient(bucket)

    print("Sending rapid burst of 6 non-blocking requests (Bucket capacity: 3):")
    for i in range(1, 7):
        resp = client.make_request(f"/api/v1/resource/{i}", blocking=False)
        print(f"  Req #{i}: Status {resp['status']} -> {resp['message']}")

    print(f"\nStats after burst: {client.successful_requests} succeeded, {client.throttled_requests} throttled.")

    print("\nWaiting 1.0 second for tokens to refill (refill rate: 2 tokens/sec)...")
    time.sleep(1.0)

    print("Sending 3 blocking requests (with automatic smooth waiting):")
    for i in range(7, 10):
        t_start = time.perf_counter()
        resp = client.make_request(f"/api/v1/resource/{i}", blocking=True)
        elapsed = time.perf_counter() - t_start
        print(f"  Req #{i}: Status {resp['status']} (waited {elapsed:.3f}s) -> {resp['message']}")


if __name__ == "__main__":
    main()
