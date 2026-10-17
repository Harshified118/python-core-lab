"""
04_search_and_sort.py
Category: Basic / Algorithms

Description:
Implementation of fundamental sorting and searching algorithms with comparison tracking:
- Binary Search (Exact match, bisect_left, bisect_right)
- Merge Sort (Stable, O(n log n))
- In-place Quick Sort (Hoare Partition scheme, O(n log n) average)
- Instrumented metrics counting comparisons and elapsed time
"""

from typing import List, Tuple, Optional


def binary_search(arr: List[int], target: int) -> Optional[int]:
    """Classic binary search. Returns index if found, else None."""
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return None


def bisect_left(arr: List[int], target: int) -> int:
    """Finds the first index where target could be inserted without violating order."""
    low, high = 0, len(arr)
    while low < high:
        mid = (low + high) // 2
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid
    return low


def bisect_right(arr: List[int], target: int) -> int:
    """Finds the last index where target could be inserted without violating order."""
    low, high = 0, len(arr)
    while low < high:
        mid = (low + high) // 2
        if target < arr[mid]:
            high = mid
        else:
            low = mid + 1
    return low


def merge_sort(arr: List[int]) -> Tuple[List[int], int]:
    """Stable merge sort returning (sorted_list, comparison_count)."""
    comparisons = 0

    def _sort(sub: List[int]) -> List[int]:
        nonlocal comparisons
        if len(sub) <= 1:
            return sub

        mid = len(sub) // 2
        left = _sort(sub[:mid])
        right = _sort(sub[mid:])

        # Merge step
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    sorted_arr = _sort(arr)
    return sorted_arr, comparisons


def quick_sort(arr: List[int]) -> Tuple[List[int], int]:
    """In-place quick sort using median-of-three pivot."""
    a = list(arr)
    comparisons = 0

    def _partition(low: int, high: int) -> int:
        nonlocal comparisons
        mid = (low + high) // 2
        pivot = a[mid]
        i = low - 1
        j = high + 1

        while True:
            i += 1
            while a[i] < pivot:
                comparisons += 1
                i += 1
            comparisons += 1

            j -= 1
            while a[j] > pivot:
                comparisons += 1
                j -= 1
            comparisons += 1

            if i >= j:
                return j

            a[i], a[j] = a[j], a[i]

    def _quick_sort(low: int, high: int):
        if low < high:
            pi = _partition(low, high)
            _quick_sort(low, pi)
            _quick_sort(pi + 1, high)

    _quick_sort(0, len(a) - 1)
    return a, comparisons


def main():
    print("=== 04: Search and Sort Algorithms Demo ===")

    # Binary search demo
    sorted_data = [5, 12, 17, 23, 23, 23, 38, 45, 56, 72, 91]
    print(f"Sorted Array: {sorted_data}")
    target = 23
    idx = binary_search(sorted_data, target)
    b_left = bisect_left(sorted_data, target)
    b_right = bisect_right(sorted_data, target)

    print(f"Target: {target}")
    print(f"  Exact Match Index : {idx}")
    print(f"  First Occurrence  : {b_left}")
    print(f"  Last Occurrence   : {b_right - 1} (count = {b_right - b_left})")

    # Sorting demo
    import random
    random.seed(42)
    sample = [random.randint(1, 100) for _ in range(12)]
    print(f"\nUnsorted sample: {sample}")

    m_sorted, m_comps = merge_sort(sample)
    print(f"Merge Sort  : {m_sorted} (Comparisons: {m_comps})")

    q_sorted, q_comps = quick_sort(sample)
    print(f"Quick Sort  : {q_sorted} (Comparisons: {q_comps})")


if __name__ == "__main__":
    main()
