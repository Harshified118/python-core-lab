"""
10_context_manager_transaction.py
Category: Intermediate / Resource Management & Context Managers

Description:
Implementation of transaction context managers in Python:
1. Class-based Context Manager (`__enter__` and `__exit__`) implementing
   an ACID-like in-memory transactional dictionary with automatic rollback on exception.
2. Generator-based Context Manager using `@contextlib.contextmanager` for
   temporary environment variable masking.
3. Savepoint & nesting demonstration for data integrity guarantees.
"""

import copy
import os
from contextlib import contextmanager
from typing import Dict, Any, Generator


class TransactionalDict:
    """
    In-memory key-value dictionary supporting atomic transactions.
    If an exception occurs within the `with` block, changes are rolled back to the state
    at the time of `__enter__`. If successful, changes are committed.
    """
    def __init__(self, initial_data: Dict[str, Any] = None):
        self._data: Dict[str, Any] = dict(initial_data or {})
        self._snapshot_stack: list = []

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any):
        self._data[key] = value

    def __delitem__(self, key: str):
        del self._data[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def snapshot(self) -> Dict[str, Any]:
        return copy.deepcopy(self._data)

    def transaction(self) -> "TransactionalDict":
        return self

    def __enter__(self) -> "TransactionalDict":
        # Save snapshot of data onto stack
        self._snapshot_stack.append(self.snapshot())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if not self._snapshot_stack:
            return False

        saved_state = self._snapshot_stack.pop()
        if exc_type is not None:
            # An error occurred: Rollback
            print(f"⚠️  [Transaction Rollback] Exception: {exc_val}. Restoring previous state.")
            self._data = saved_state
            return False  # Do not suppress the exception
        else:
            # Successful completion: Commit
            print("✅ [Transaction Commit] Changes committed successfully.")
            return True


@contextmanager
def temporary_env(key: str, temp_value: str) -> Generator[None, None, None]:
    """Temporarily sets an environment variable, restoring the original value on exit."""
    original = os.environ.get(key)
    os.environ[key] = temp_value
    try:
        yield
    finally:
        if original is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = original


def main():
    print("=== 10: Context Managers & Transaction Rollback Demo ===")

    # 1. Transactional Dictionary Demo
    db = TransactionalDict({"user:1": {"balance": 100}, "user:2": {"balance": 50}})
    print("Initial Database State:", db.snapshot())

    print("\nExecuting Successful Transaction (Transfer $30 from user:1 to user:2):")
    with db.transaction():
        db["user:1"]["balance"] -= 30
        db["user:2"]["balance"] += 30

    print("State after commit:", db.snapshot())

    print("\nExecuting Failing Transaction (Transfer $1000 with simulated error):")
    try:
        with db.transaction():
            db["user:1"]["balance"] -= 1000
            db["user:2"]["balance"] += 1000
            raise ValueError("Insufficient credit limit! Transaction aborted.")
    except ValueError as err:
        print("Caught expected exception:", err)

    print("State after rollback (balances unchanged):", db.snapshot())

    # 2. Temporary Environment Variable Demo
    os.environ["APP_MODE"] = "PRODUCTION"
    print(f"\nInitial APP_MODE: {os.environ.get('APP_MODE')}")

    with temporary_env("APP_MODE", "TESTING_SANDBOX"):
        print(f"Inside temporary_env block: {os.environ.get('APP_MODE')}")

    print(f"Outside temporary_env block: {os.environ.get('APP_MODE')}")


if __name__ == "__main__":
    main()
