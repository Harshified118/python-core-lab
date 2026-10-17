"""
05_expense_tracker.py
Category: Basic / Practical CLI Application

Description:
A structured personal finance & expense manager:
- Record, tag, and categorize expenditures
- Date parsing and validation (ISO-8601 format: YYYY-MM-DD)
- Categorical aggregation and budget threshold alerts
- Export and import to JSON
"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional


class ExpenseTracker:
    def __init__(self, budget_limit: float = 1000.0):
        self.expenses: List[Dict[str, Any]] = []
        self.budget_limit = budget_limit

    def add_expense(
        self,
        amount: float,
        category: str,
        description: str,
        date_str: Optional[str] = None,
    ) -> Dict[str, Any]:
        if amount <= 0:
            raise ValueError("Expense amount must be positive.")

        if date_str:
            # Validate ISO date format
            datetime.strptime(date_str, "%Y-%m-%d")
            entry_date = date_str
        else:
            entry_date = datetime.now().strftime("%Y-%m-%d")

        expense = {
            "id": len(self.expenses) + 1,
            "amount": round(float(amount), 2),
            "category": category.strip().capitalize(),
            "description": description.strip(),
            "date": entry_date,
        }
        self.expenses.append(expense)
        return expense

    def total_spending(self) -> float:
        return sum(e["amount"] for e in self.expenses)

    def spending_by_category(self) -> Dict[str, float]:
        breakdown: Dict[str, float] = {}
        for e in self.expenses:
            cat = e["category"]
            breakdown[cat] = round(breakdown.get(cat, 0.0) + e["amount"], 2)
        return breakdown

    def filter_by_category(self, category: str) -> List[Dict[str, Any]]:
        cat_lower = category.strip().lower()
        return [e for e in self.expenses if e["category"].lower() == cat_lower]

    def check_budget_status(self) -> Dict[str, Any]:
        spent = self.total_spending()
        remaining = self.budget_limit - spent
        is_exceeded = spent > self.budget_limit
        percent_used = (spent / self.budget_limit) * 100.0 if self.budget_limit > 0 else 100.0

        return {
            "budget_limit": self.budget_limit,
            "total_spent": round(spent, 2),
            "remaining": round(remaining, 2),
            "percent_used": round(percent_used, 1),
            "is_exceeded": is_exceeded,
        }

    def to_json(self) -> str:
        return json.dumps(
            {"budget_limit": self.budget_limit, "expenses": self.expenses},
            indent=2,
        )

    @classmethod
    def from_json(cls, json_data: str) -> "ExpenseTracker":
        data = json.loads(json_data)
        tracker = cls(budget_limit=data.get("budget_limit", 1000.0))
        tracker.expenses = data.get("expenses", [])
        return tracker


def main():
    print("=== 05: Personal Expense Tracker Demo ===")
    tracker = ExpenseTracker(budget_limit=500.0)

    # Add sample expenditures
    tracker.add_expense(45.50, "Food", "Grocery shopping", "2026-10-10")
    tracker.add_expense(120.00, "Utilities", "Electricity bill", "2026-10-12")
    tracker.add_expense(15.99, "Entertainment", "Streaming subscription", "2026-10-14")
    tracker.add_expense(85.00, "Food", "Dinner with colleagues", "2026-10-15")
    tracker.add_expense(60.00, "Transport", "Train monthly pass", "2026-10-16")

    print(f"\nTotal Expenditures: ${tracker.total_spending():.2f}")

    print("\nCategorical Breakdown:")
    for cat, total in tracker.spending_by_category().items():
        print(f"  - {cat:<15}: ${total:>6.2f}")

    status = tracker.check_budget_status()
    print(f"\nBudget Status:")
    print(f"  Limit        : ${status['budget_limit']:.2f}")
    print(f"  Total Spent  : ${status['total_spent']:.2f} ({status['percent_used']}%)")
    print(f"  Remaining    : ${status['remaining']:.2f}")
    print(f"  Exceeded?    : {'YES ⚠️' if status['is_exceeded'] else 'NO (Within Budget) ✅'}")

    # JSON export preview
    print("\nExported JSON Snapshot:")
    print(tracker.to_json())


if __name__ == "__main__":
    main()
