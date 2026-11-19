import json
import os

from src.analytics import ExpenseAnalytics


BUDGET_FILE = "data/budgets.json"


class BudgetManager:

    def __init__(self, expense_manager):

        self.expense_manager = expense_manager

        self.analytics = ExpenseAnalytics(expense_manager)

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(BUDGET_FILE):

            with open(BUDGET_FILE, "w") as file:

                json.dump({}, file, indent=4)

    # Load budgets
    def load_budgets(self):

        try:

            with open(BUDGET_FILE, "r") as file:

                return json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):

            return {}

    # Save budgets
    def save_budgets(self, budgets):

        with open(BUDGET_FILE, "w") as file:

            json.dump(budgets, file, indent=4)

    # Set budget
    def set_budget(self, category, amount):

        try:

            amount = float(amount)

            if amount <= 0:

                print("Budget must be greater than zero.")

                return False

        except ValueError:

            print("Invalid budget amount.")

            return False

        budgets = self.load_budgets()

        budgets[category] = amount

        self.save_budgets(budgets)

        print(
            f"\nBudget set successfully for {category}: ₹{amount:,.2f}"
        )

        return True

    # Calculate spending for category
    def category_spending(self, category):

        df = self.analytics.get_data()

        if df.empty:

            return 0

        return df[df["category"] == category]["amount"].sum()

    # Check budget
    def check_budget(self, category):

        budgets = self.load_budgets()

        if category not in budgets:

            print("No budget set for this category.")

            return

        budget = budgets[category]

        spent = self.category_spending(category)

        remaining = budget - spent

        percentage = (spent / budget) * 100

        print("\n========== BUDGET STATUS ==========")

        print(f"Category        : {category}")

        print(f"Budget          : ₹{budget:,.2f}")

        print(f"Spent           : ₹{spent:,.2f}")

        print(f"Remaining       : ₹{remaining:,.2f}")

        print(f"Utilization     : {percentage:.2f}%")

        if spent > budget:

            print("\n⚠️ ALERT: Budget exceeded!")

        elif percentage >= 80:

            print("\n⚠️ WARNING: You have used 80% of your budget.")

        else:

            print("\n✅ You are within your budget.")

    # Display all budgets
    def display_budgets(self):

        budgets = self.load_budgets()

        if not budgets:

            print("\nNo budgets configured.")

            return

        print("\n========== ALL BUDGETS ==========")

        for category, amount in budgets.items():

            spent = self.category_spending(category)

            remaining = amount - spent

            percentage = (spent / amount) * 100

            print(f"\nCategory       : {category}")

            print(f"Budget         : ₹{amount:,.2f}")

            print(f"Spent          : ₹{spent:,.2f}")

            print(f"Remaining      : ₹{remaining:,.2f}")

            print(f"Used           : {percentage:.2f}%")

            if spent > amount:

                print("Status         : EXCEEDED")

            elif percentage >= 80:

                print("Status         : WARNING")

            else:

                print("Status         : SAFE")