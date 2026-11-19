import pandas as pd
import os
from datetime import datetime

from src.validators import (
    validate_date,
    validate_amount,
    validate_category,
    validate_payment_method
)

DATA_FILE = "data/expenses.csv"


class ExpenseManager:

    def __init__(self):
        self.data_file = DATA_FILE

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.data_file):
            columns = [
                "expense_id",
                "date",
                "category",
                "description",
                "amount",
                "payment_method"
            ]

            pd.DataFrame(columns=columns).to_csv(
                self.data_file,
                index=False
            )

    def load_expenses(self):

        try:
            df = pd.read_csv(self.data_file)

            if df.empty:
                return df

            df["date"] = pd.to_datetime(
                df["date"],
                errors="coerce"
            )

            return df

        except (FileNotFoundError, pd.errors.EmptyDataError):
            return pd.DataFrame()

    def generate_expense_id(self):

        df = self.load_expenses()

        if df.empty:
            return "EXP001"

        numbers = []

        for expense_id in df["expense_id"].astype(str):

            try:
                number = int(expense_id.replace("EXP", ""))
                numbers.append(number)

            except ValueError:
                continue

        next_number = max(numbers, default=0) + 1

        return f"EXP{next_number:03d}"

    def add_expense(
        self,
        date,
        category,
        description,
        amount,
        payment_method
    ):

        # Date validation
        if not validate_date(date):
            print("Invalid date! Use YYYY-MM-DD and no future date.")
            return False

        # Amount validation
        if not validate_amount(amount):
            print("Invalid amount! Enter a positive number.")
            return False

        # Category validation
        if not validate_category(category):
            print("Invalid category!")
            return False

        # Payment validation
        if not validate_payment_method(payment_method):
            print("Invalid payment method!")
            return False

        amount = float(amount)

        expense_id = self.generate_expense_id()

        new_expense = {
            "expense_id": expense_id,
            "date": date,
            "category": category,
            "description": description,
            "amount": amount,
            "payment_method": payment_method
        }

        new_df = pd.DataFrame([new_expense])

        new_df.to_csv(
            self.data_file,
            mode="a",
            header=False,
            index=False
        )

        print(f"\nExpense added successfully! ID: {expense_id}")

        return True

    def display_expenses(self):

        df = self.load_expenses()

        if df.empty:
            print("\nNo expenses recorded yet.")
            return

        print("\n========== EXPENSE RECORDS ==========\n")

        print(df.to_string(index=False))

        print("\n====================================")

    def delete_expense(self, expense_id):

        df = self.load_expenses()

        if df.empty:
            print("No expenses available.")
            return False

        if expense_id not in df["expense_id"].astype(str).values:
            print("Expense ID not found.")
            return False

        df = df[df["expense_id"] != expense_id]

        df["date"] = df["date"].dt.strftime("%Y-%m-%d")

        df.to_csv(
            self.data_file,
            index=False
        )

        print(f"Expense {expense_id} deleted successfully!")

        return True