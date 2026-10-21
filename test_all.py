"""
test_all.py
Automated test suite verifying all 10 programs in python-core-lab.
"""

import unittest
import os
import tempfile
from collections import OrderedDict

# Program imports
from importlib import import_module

p01 = import_module("01_text_analyzer")
p02 = import_module("02_matrix_operations")
p03 = import_module("03_password_utility")
p04 = import_module("04_search_and_sort")
p05 = import_module("05_expense_tracker")
p06 = import_module("06_custom_decorators")
p07 = import_module("07_producer_consumer")
p08 = import_module("08_duplicate_file_finder")
p09 = import_module("09_rate_limited_client")
p10 = import_module("10_context_manager_transaction")
p11 = import_module("11_graph_traversal")


class TestPythonCoreLab(unittest.TestCase):

    def test_01_text_analyzer(self):
        sample = "Hello world! This is Python. Python is fast."
        res = p01.analyze_text(sample)
        self.assertEqual(res["sentences"], 3)
        self.assertGreater(res["words"], 0)
        self.assertIn("python", [w[0] for w in res["top_words"]])

    def test_02_matrix_operations(self):
        a = [[1, 2], [3, 4]]
        b = [[2, 0], [1, 2]]
        self.assertEqual(p02.add_matrices(a, b), [[3, 2], [4, 6]])
        self.assertEqual(p02.multiply_matrices(a, b), [[4, 4], [10, 8]])
        self.assertEqual(p02.transpose(a), [[1, 3], [2, 4]])
        self.assertEqual(p02.determinant_2x2(a), -2)

    def test_03_password_utility(self):
        pwd = p03.generate_password(length=16)
        self.assertEqual(len(pwd), 16)
        eval_res = p03.evaluate_strength(pwd)
        self.assertIn(eval_res["rating"], ["Strong", "Very Strong"])
        self.assertGreater(p03.calculate_entropy(pwd), 50.0)

    def test_04_search_and_sort(self):
        data = [1, 3, 5, 7, 9, 11]
        self.assertEqual(p04.binary_search(data, 7), 3)
        self.assertIsNone(p04.binary_search(data, 4))
        unsorted = [9, 1, 5, 2, 8, 3]
        s_m, _ = p04.merge_sort(unsorted)
        s_q, _ = p04.quick_sort(unsorted)
        self.assertEqual(s_m, [1, 2, 3, 5, 8, 9])
        self.assertEqual(s_q, [1, 2, 3, 5, 8, 9])

    def test_05_expense_tracker(self):
        tracker = p05.ExpenseTracker(budget_limit=200.0)
        tracker.add_expense(50.0, "Food", "Groceries")
        tracker.add_expense(100.0, "Tech", "Headphones")
        self.assertEqual(tracker.total_spending(), 150.0)
        status = tracker.check_budget_status()
        self.assertFalse(status["is_exceeded"])
        self.assertEqual(status["remaining"], 50.0)

    def test_06_custom_decorators(self):
        calls = 0
        @p06.lru_cache_custom(maxsize=2)
        def square(x):
            nonlocal calls
            calls += 1
            return x * x

        self.assertEqual(square(4), 16)
        self.assertEqual(square(4), 16)
        self.assertEqual(calls, 1)  # Cached
        self.assertEqual(square.cache_info()["hits"], 1)

    def test_07_producer_consumer(self):
        pipeline = p07.ProducerConsumerPipeline(num_consumers=2, max_queue_size=4)
        pipeline.start()
        for i in range(4):
            pipeline.submit_task(p07.Task(i, f"item_{i}", 0.01))
        pipeline.shutdown()
        self.assertEqual(len(pipeline.results), 4)

    def test_08_duplicate_file_finder(self):
        with tempfile.TemporaryDirectory() as td:
            p1 = os.path.join(td, "a.txt")
            p2 = os.path.join(td, "b.txt")
            content = b"Exact identical binary payload" * 10
            with open(p1, "wb") as f: f.write(content)
            with open(p2, "wb") as f: f.write(content)
            dupes = p08.find_duplicates(td)
            self.assertEqual(len(dupes), 1)

    def test_09_rate_limited_client(self):
        bucket = p09.TokenBucket(capacity=2.0, fill_rate=10.0)
        client = p09.SimulatedApiClient(bucket)
        self.assertEqual(client.make_request("/res/1")["status"], 200)
        self.assertEqual(client.make_request("/res/2")["status"], 200)
        self.assertEqual(client.make_request("/res/3")["status"], 429)

    def test_10_context_manager_transaction(self):
        db = p10.TransactionalDict({"account": 100})
        try:
            with db.transaction():
                db["account"] = 500
                raise RuntimeError("Force crash")
        except RuntimeError:
            pass
        self.assertEqual(db["account"], 100)  # Rolled back successfully

    def test_11_graph_traversal(self):
        # 1. Undirected BFS, DFS, and Shortest Path
        g = p11.Graph(directed=False)
        for u, v in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]:
            g.add_edge(u, v)

        self.assertEqual(g.bfs("A"), ["A", "B", "C", "D"])
        self.assertEqual(g.dfs("A"), ["A", "B", "D", "C"])
        self.assertEqual(g.shortest_path_unweighted("A", "D"), ["A", "B", "D"])
        self.assertTrue(g.has_cycle())

        # 2. Directed Acyclic Graph & Topological Sort
        dag = p11.Graph(directed=True)
        dag.add_edge("1", "2")
        dag.add_edge("2", "3")
        dag.add_edge("1", "3")
        self.assertFalse(dag.has_cycle())
        self.assertEqual(dag.topological_sort(), ["1", "2", "3"])

        # 3. Directed Cyclic Graph
        cyclic = p11.Graph(directed=True)
        cyclic.add_edge("X", "Y")
        cyclic.add_edge("Y", "Z")
        cyclic.add_edge("Z", "X")
        self.assertTrue(cyclic.has_cycle())
        self.assertIsNone(cyclic.topological_sort())


if __name__ == "__main__":
    unittest.main()
