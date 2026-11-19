import matplotlib.pyplot as plt
import pandas as pd
import os

from src.analytics import ExpenseAnalytics


class ExpenseVisualizer:

    def __init__(self, expense_manager):

        self.analytics = ExpenseAnalytics(expense_manager)

        os.makedirs("reports/charts", exist_ok=True)

    # Category pie chart
    def category_pie_chart(self):

        data = self.analytics.category_summary()

        if data.empty:
            print("No data available.")
            return

        plt.figure(figsize=(9, 7))

        plt.pie(
            data.values,
            labels=data.index,
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title("Expense Distribution by Category")

        plt.tight_layout()

        plt.savefig("reports/charts/category_pie.png")

        plt.show()

    # Category bar chart
    def category_bar_chart(self):

        data = self.analytics.category_summary()

        if data.empty:
            print("No data available.")
            return

        plt.figure(figsize=(10, 6))

        plt.bar(data.index, data.values)

        plt.title("Category-wise Expenses")

        plt.xlabel("Category")

        plt.ylabel("Amount (₹)")

        plt.xticks(rotation=45)

        plt.tight_layout()

        plt.savefig("reports/charts/category_bar.png")

        plt.show()

    # Monthly trend
    def monthly_trend_chart(self):

        data = self.analytics.monthly_summary()

        if data.empty:
            print("No data available.")
            return

        data.index = data.index.astype(str)

        plt.figure(figsize=(10, 6))

        plt.plot(
            data.index,
            data.values,
            marker="o"
        )

        plt.title("Monthly Expense Trend")

        plt.xlabel("Month")

        plt.ylabel("Amount (₹)")

        plt.xticks(rotation=45)

        plt.grid(True)

        plt.tight_layout()

        plt.savefig("reports/charts/monthly_trend.png")

        plt.show()

    # Payment method chart
    def payment_chart(self):

        data = self.analytics.payment_summary()

        if data.empty:
            print("No data available.")
            return

        plt.figure(figsize=(9, 6))

        plt.bar(
            data.index,
            data.values
        )

        plt.title("Expenses by Payment Method")

        plt.xlabel("Payment Method")

        plt.ylabel("Amount (₹)")

        plt.xticks(rotation=30)

        plt.tight_layout()

        plt.savefig("reports/charts/payment_methods.png")

        plt.show()

    # Generate all charts
    def generate_all_charts(self):

        print("\nGenerating visualizations...")

        self.category_pie_chart()

        self.category_bar_chart()

        self.monthly_trend_chart()

        self.payment_chart()

        print("\nAll charts generated successfully!")

        print("Charts saved in reports/charts/")