import random
import pandas as pd
from datetime import datetime, timedelta
import os

from src.validators import CATEGORIES, PAYMENT_METHODS


class SyntheticDataGenerator:

    def __init__(self):

        self.data_file = "data/expenses.csv"

        self.descriptions = {

            "Food": [
                "Restaurant lunch",
                "Online food order",
                "Breakfast",
                "Coffee",
                "Dinner",
                "Snacks"
            ],

            "Transportation": [
                "Auto rickshaw",
                "Bus ticket",
                "Fuel",
                "Cab ride",
                "Train ticket"
            ],

            "Shopping": [
                "Clothing",
                "Grocery shopping",
                "Electronics",
                "Online shopping"
            ],

            "Bills": [
                "Electricity bill",
                "Internet bill",
                "Mobile recharge",
                "Water bill"
            ],

            "Education": [
                "Books",
                "Online course",
                "Stationery",
                "Exam fees"
            ],

            "Healthcare": [
                "Medicine",
                "Doctor consultation",
                "Medical tests"
            ],

            "Entertainment": [
                "Movie ticket",
                "OTT subscription",
                "Gaming",
                "Event ticket"
            ],

            "Travel": [
                "Hotel booking",
                "Trip expenses",
                "Tour package",
                "Travel ticket"
            ],

            "Other": [
                "Miscellaneous expense",
                "Personal expense",
                "Unexpected expense"
            ]
        }

    def generate_data(self, number_of_records=100):

        records = []

        today = datetime.today()

        for i in range(number_of_records):

            category = random.choice(CATEGORIES)

            random_days = random.randint(0, 180)

            expense_date = today - timedelta(days=random_days)

            amount_ranges = {

                "Food": (50, 1500),

                "Transportation": (30, 2000),

                "Shopping": (100, 10000),

                "Bills": (200, 5000),

                "Education": (100, 5000),

                "Healthcare": (100, 3000),

                "Entertainment": (100, 2500),

                "Travel": (500, 15000),

                "Other": (50, 3000)
            }

            minimum, maximum = amount_ranges[category]

            amount = round(
                random.uniform(minimum, maximum),
                2
            )

            description = random.choice(
                self.descriptions[category]
            )

            payment_method = random.choice(
                PAYMENT_METHODS
            )

            record = {

                "expense_id": f"EXP{str(i + 1).zfill(3)}",

                "date": expense_date.strftime("%Y-%m-%d"),

                "category": category,

                "description": description,

                "amount": amount,

                "payment_method": payment_method
            }

            records.append(record)

        df = pd.DataFrame(records)

        return df

    def save_data(self, number_of_records=100, replace_existing=False):

        df = self.generate_data(number_of_records)

        os.makedirs("data", exist_ok=True)

        if replace_existing:

            df.to_csv(self.data_file, index=False)

        else:

            if os.path.exists(self.data_file):

                existing = pd.read_csv(self.data_file)

                if not existing.empty:

                    start_id = len(existing) + 1

                    df["expense_id"] = [
                        f"EXP{str(i).zfill(3)}"
                        for i in range(
                            start_id,
                            start_id + len(df)
                        )
                    ]

                    df = pd.concat(
                        [existing, df],
                        ignore_index=True
                    )

            df.to_csv(self.data_file, index=False)

        print(
            f"\n{number_of_records} synthetic expenses generated successfully!"
        )

        print(f"Saved to: {self.data_file}")

        return df