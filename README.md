# Python Core Lab (`python-core-lab`)

> A curated collection of 10 foundational to intermediate Python programs covering data structures, algorithmic efficiency, thread concurrency, systems programming, and design patterns.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests: Passing](https://img.shields.io/badge/Tests-10%20Passing-brightgreen.svg)]()

---

## 📚 Overview & Table of Contents

| # | Program | Level | Focus & Key Concepts |
|---|---|---|---|
| **01** | [`01_text_analyzer.py`](./01_text_analyzer.py) | Basic | String tokenization, lexical diversity, reading time calculation, top-N frequencies |
| **02** | [`02_matrix_operations.py`](./02_matrix_operations.py) | Basic | Pure-Python matrix arithmetic, transposition, 90° rotation, 2x2/3x3 determinants |
| **03** | [`03_password_utility.py`](./03_password_utility.py) | Basic | Cryptographic entropy, password & passphrase generation with `secrets`, compliance scoring |
| **04** | [`04_search_and_sort.py`](./04_search_and_sort.py) | Basic | Binary search (exact & bounds), Merge sort, Quick sort with comparison instrumentation |
| **05** | [`05_expense_tracker.py`](./05_expense_tracker.py) | Basic | Personal expenditure tracker, category aggregations, budget alarms, JSON I/O |
| **06** | [`06_custom_decorators.py`](./06_custom_decorators.py) | Intermediate | `@timer`, exponential backoff `@retry`, `@lru_cache_custom`, runtime `@validate_types` |
| **07** | [`07_producer_consumer.py`](./07_producer_consumer.py) | Intermediate | Multithreaded pipeline, bounded `queue.Queue`, poison pill protocol, worker distribution |
| **08** | [`08_duplicate_file_finder.py`](./08_duplicate_file_finder.py) | Intermediate | Three-tier duplicate scanner (size grouping, 4KB partial hash, full chunked SHA-256) |
| **09** | [`09_rate_limited_client.py`](./09_rate_limited_client.py) | Intermediate | Token Bucket rate limiter, burst handling, constant replenishment, simulated API backpressure |
| **10** | [`10_context_manager_transaction.py`](./10_context_manager_transaction.py) | Intermediate | Class-based atomic transaction dictionary with automatic rollback on exception & `@contextmanager` |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher (No third-party packages required — uses standard library).

### Installation
Clone the repository:
```bash
git clone https://github.com/Harshified118/python-core-lab.git
cd python-core-lab
```

### Running the Full Test Suite
```bash
python3 test_all.py
```

### Running Individual Programs
Each script contains an executable demonstration block:
```bash
python3 01_text_analyzer.py
python3 02_matrix_operations.py
python3 03_password_utility.py
python3 04_search_and_sort.py
python3 05_expense_tracker.py
python3 06_custom_decorators.py
python3 07_producer_consumer.py
python3 08_duplicate_file_finder.py
python3 09_rate_limited_client.py
python3 10_context_manager_transaction.py
```

---

## 🧠 Detailed Program Summaries

### 01. Text Analyzer & Readability Metric
Analyzes text input to produce structural metrics:
- Counts words, sentences, and paragraphs via regular expressions.
- Measures vocabulary density (lexical diversity) and average sentence complexity.
- Estimates reading time based on standard 200 words-per-minute pace.
- Extracts dominant keywords while filtering common stop words.

### 02. Matrix Arithmetic & Transformations
Provides linear algebra operations without external dependencies:
- Addition and scalar scaling.
- Matrix multiplication checking inner dimension compatibility ($O(n^3)$).
- In-place transposition and 90-degree clockwise geometric rotation.
- Determinant calculation for $2 \times 2$ and $3 \times 3$ matrices using cofactor expansion.

### 03. Password & Passphrase Security Utility
Security generator and strength auditing engine:
- Evaluates Shannon bit entropy ($E = L \cdot \log_2(R)$).
- Generates cryptographically secure passwords using the operating system's CSPRNG via `secrets`.
- Generates high-entropy multi-word passphrases using Diceware-style lists.

### 04. Instrumented Search & Sort Routines
Demonstrates foundational algorithms alongside runtime comparison counts:
- Binary Search with exact index, `bisect_left`, and `bisect_right`.
- Merge Sort: Stable divide-and-conquer algorithm with guaranteed $O(n \log n)$ complexity.
- Quick Sort: In-place partitioning scheme with median pivot selection.

### 05. CLI Personal Expense Tracker
A practical financial tracking module:
- Logs date-stamped expenses across categories (Food, Utilities, Entertainment, etc.).
- Computes categorical distributions and budget threshold alerts.
- Serializes and deserializes records to and from structured JSON.

### 06. Production Metaprogramming Decorators
Advanced Python metaprogramming and decorator patterns:
- `@timer`: Precision performance profiling with `time.perf_counter`.
- `@retry`: Handles transient failures with exponential backoff and jitter.
- `@lru_cache_custom`: Memoizes expensive calls using an `OrderedDict` with size bounding.
- `@validate_types`: Enforces runtime type conformance against type hints via `inspect.signature`.

### 07. Multi-Threaded Producer-Consumer Pipeline
Concurrent pipeline design for CPU/IO work balancing:
- Bounded thread-safe queue (`queue.Queue`) preventing memory overflow.
- Multiple worker threads processing items concurrently.
- Clean shutdown protocol using sentinel "poison pill" markers and thread joining.

### 08. Scalable Duplicate File Scanner
Efficient filesystem duplicate detection:
- Stage 1: Fast filtering by file size (files with unique sizes are skipped).
- Stage 2: 4KB initial block fingerprint hash to eliminate non-matching candidates.
- Stage 3: Streaming chunked SHA-256 computation to confirm duplicates without large memory allocations.

### 09. Rate-Limiting & API Client
Implements classic network traffic shaping algorithms:
- **Token Bucket**: Allows bursts up to bucket capacity and refills at a steady rate.
- Simulated API client supporting non-blocking (429 Too Many Requests) and blocking wait modes.

### 10. Atomic Context Managers & Rollback Transactions
Context managers implementing transaction isolation:
- Class-based context manager (`__enter__` and `__exit__`) tracking state snapshots with automatic rollback upon exceptions.
- Generator-based context managers (`@contextlib.contextmanager`) for safe temporary resource overrides.

---

## 👤 Author

**Harsh Kr** ([@Harshified118](https://github.com/Harshified118))
- B-Tech CSE Student
- Focus: Python, DSA, JavaScript & Modern Web Systems

---

## 📄 License
This project is licensed under the MIT License.
