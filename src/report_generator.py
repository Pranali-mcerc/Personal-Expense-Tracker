import os
import pandas as pd

from src.analytics import ExpenseAnalytics


class ReportGenerator:

    def __init__(self, expense_manager):

        self.manager = expense_manager

        self.analytics = ExpenseAnalytics(expense_manager)

        os.makedirs("reports", exist_ok=True)

    # Export all expenses
    def export_all_expenses(self):

        df = self.manager.load_expenses()

        if df.empty:

            print("No data available to export.")

            return

        df["date"] = df["date"].dt.strftime("%Y-%m-%d")

        filepath = "reports/all_expenses_report.csv"

        df.to_csv(filepath, index=False)

        print(f"\nReport exported successfully: {filepath}")

    # Export category report
    def export_category_report(self):

        data = self.analytics.category_summary()

        if data.empty:

            print("No data available.")

            return

        report = data.reset_index()

        report.columns = ["Category", "Total Amount"]

        filepath = "reports/category_report.csv"

        report.to_csv(filepath, index=False)

        print(f"\nCategory report exported: {filepath}")

    # Export monthly report
    def export_monthly_report(self):

        data = self.analytics.monthly_summary()

        if data.empty:

            print("No data available.")

            return

        report = data.reset_index()

        report.columns = ["Month", "Total Expenses"]

        report["Month"] = report["Month"].astype(str)

        filepath = "reports/monthly_report.csv"

        report.to_csv(filepath, index=False)

        print(f"\nMonthly report exported: {filepath}")

    # Export payment report
    def export_payment_report(self):

        data = self.analytics.payment_summary()

        if data.empty:

            print("No data available.")

            return

        report = data.reset_index()

        report.columns = ["Payment Method", "Total Amount"]

        filepath = "reports/payment_report.csv"

        report.to_csv(filepath, index=False)

        print(f"\nPayment report exported: {filepath}")

    # Generate all reports
    def generate_all_reports(self):

        print("\nGenerating reports...")

        self.export_all_expenses()

        self.export_category_report()

        self.export_monthly_report()

        self.export_payment_report()

        print("\nAll reports generated successfully!")