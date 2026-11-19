import pandas as pd


class ExpenseAnalytics:

    def __init__(self, expense_manager):

        self.manager = expense_manager

    def get_data(self):

        df = self.manager.load_expenses()

        if df.empty:
            return df

        df["amount"] = pd.to_numeric(
            df["amount"],
            errors="coerce"
        )

        df = df.dropna(subset=["amount"])

        return df

    # Total spending
    def total_expenses(self):

        df = self.get_data()

        if df.empty:
            return 0

        return df["amount"].sum()

    # Average spending
    def average_expense(self):

        df = self.get_data()

        if df.empty:
            return 0

        return df["amount"].mean()

    # Highest expense
    def highest_expense(self):

        df = self.get_data()

        if df.empty:
            return None

        return df.loc[df["amount"].idxmax()]

    # Lowest expense
    def lowest_expense(self):

        df = self.get_data()

        if df.empty:
            return None

        return df.loc[df["amount"].idxmin()]

    # Category analysis
    def category_summary(self):

        df = self.get_data()

        if df.empty:
            return pd.DataFrame()

        summary = df.groupby("category")["amount"].sum()

        summary = summary.sort_values(ascending=False)

        return summary

    # Monthly spending analysis
    def monthly_summary(self):

        df = self.get_data()

        if df.empty:
            return pd.DataFrame()

        df["month"] = df["date"].dt.to_period("M")

        summary = df.groupby("month")["amount"].sum()

        return summary

    # Payment method analysis
    def payment_summary(self):

        df = self.get_data()

        if df.empty:
            return pd.DataFrame()

        return df.groupby("payment_method")["amount"].sum()

    # Daily spending analysis
    def daily_summary(self):

        df = self.get_data()

        if df.empty:
            return pd.DataFrame()

        return df.groupby(df["date"].dt.date)["amount"].sum()

    # Display analytics
    def display_analytics(self):

        df = self.get_data()

        if df.empty:
            print("\nNo data available for analytics.")
            return

        print("\n" + "=" * 45)
        print("           EXPENSE ANALYTICS")
        print("=" * 45)

        print(f"\nTotal Expenses   : ₹{self.total_expenses():,.2f}")
        print(f"Average Expense  : ₹{self.average_expense():,.2f}")

        highest = self.highest_expense()
        lowest = self.lowest_expense()

        print(f"\nHighest Expense  : ₹{highest['amount']:,.2f}")
        print(f"  Category       : {highest['category']}")
        print(f"  Description    : {highest['description']}")

        print(f"\nLowest Expense   : ₹{lowest['amount']:,.2f}")
        print(f"  Category       : {lowest['category']}")

        print("\n--- Category Summary ---")
        print(self.category_summary().to_string())

        print("\n--- Monthly Summary ---")
        print(self.monthly_summary().to_string())

        print("\n--- Payment Summary ---")
        print(self.payment_summary().to_string())

        print("\n" + "=" * 45)