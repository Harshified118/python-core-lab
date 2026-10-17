"""
06_custom_decorators.py
Category: Intermediate / Metaprogramming & Design Patterns

Description:
A collection of production-grade function decorators:
1. `@timer`: Measures and logs execution wall-clock time
2. `@retry`: Retries failing operations with exponential backoff and jitter
3. `@lru_cache_custom`: Memoizes function calls with capacity bounding and LRU eviction
4. `@validate_types`: Enforces runtime type inspection according to type annotations
"""

import functools
import inspect
import time
from collections import OrderedDict
from typing import Callable, Any, Type, Tuple


def timer(func: Callable) -> Callable:
    """Measures execution time of the decorated function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"⏱️  [Timer] '{func.__name__}' took {elapsed * 1000.0:.3f} ms")
        return result
    return wrapper


def retry(
    max_retries: int = 3,
    delay: float = 0.1,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
) -> Callable:
    """Retries a function upon specified exceptions with exponential backoff."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        print(f"❌ [Retry] '{func.__name__}' failed after {max_retries} attempts.")
                        raise
                    print(
                        f"⚠️  [Retry] '{func.__name__}' failed (Attempt {attempt}/{max_retries}): {e}. "
                        f"Retrying in {current_delay:.2f}s..."
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator


def lru_cache_custom(maxsize: int = 128) -> Callable:
    """Custom LRU cache using OrderedDict."""
    def decorator(func: Callable) -> Callable:
        cache: OrderedDict = OrderedDict()
        hits = 0
        misses = 0

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal hits, misses
            # Create hashable cache key
            key = (args, tuple(sorted(kwargs.items())))
            if key in cache:
                hits += 1
                cache.move_to_end(key)
                return cache[key]

            misses += 1
            result = func(*args, **kwargs)
            cache[key] = result
            if len(cache) > maxsize:
                cache.popitem(last=False)  # Evict oldest entry
            return result

        def cache_info():
            return {"hits": hits, "misses": misses, "size": len(cache), "maxsize": maxsize}

        def cache_clear():
            nonlocal hits, misses
            cache.clear()
            hits = 0
            misses = 0

        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        return wrapper
    return decorator


def validate_types(func: Callable) -> Callable:
    """Enforces argument types based on function type annotations."""
    sig = inspect.signature(func)
    parameters = sig.parameters

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        for name, value in bound.arguments.items():
            param = parameters.get(name)
            if param and param.annotation is not inspect.Parameter.empty:
                expected_type = param.annotation
                if isinstance(expected_type, type) and not isinstance(value, expected_type):
                    raise TypeError(
                        f"Argument '{name}' expected type {expected_type.__name__}, "
                        f"got {type(value).__name__} ({value!r})"
                    )

        return func(*args, **kwargs)
    return wrapper


# Demonstration Driver
def main():
    print("=== 06: Custom Decorators Demo ===")

    # 1. Timer demo
    @timer
    def compute_heavy_sum(n: int) -> int:
        return sum(i * i for i in range(n))

    compute_heavy_sum(500_000)

    # 2. Retry demo
    attempts = 0

    @retry(max_retries=3, delay=0.05, backoff=1.5, exceptions=(ConnectionError,))
    def flaky_network_call():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ConnectionError(f"Temporary network outage (attempt #{attempts})")
        return "Success on attempt #3!"

    result = flaky_network_call()
    print("Flaky call result:", result)

    # 3. LRU Cache demo
    @lru_cache_custom(maxsize=3)
    def fib(n: int) -> int:
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    print("\nComputing fib(10) with custom LRU Cache:")
    print("fib(10) =", fib(10))
    print("Cache Info:", fib.cache_info())

    # 4. Type Validation demo
    @validate_types
    def register_user(username: str, age: int) -> str:
        return f"User '{username}' registered with age {age}."

    print("\nCalling register_user with valid types:")
    print(register_user("Harsh", 18))

    print("Calling register_user with invalid age type (str instead of int):")
    try:
        register_user("Harsh", "eighteen")
    except TypeError as err:
        print("Caught expected TypeError:", err)


if __name__ == "__main__":
    main()
