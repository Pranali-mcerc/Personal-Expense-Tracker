from src.expense_manager import ExpenseManager
from src.analytics import ExpenseAnalytics
from src.visualizations import ExpenseVisualizer
from src.budget_manager import BudgetManager
from src.report_generator import ReportGenerator
from src.data_generator import SyntheticDataGenerator


# Initialize Expense Manager
manager = ExpenseManager()

# Initialize other modules with Expense Manager
analytics = ExpenseAnalytics(manager)
visualizer = ExpenseVisualizer(manager)
budget_manager = BudgetManager(manager)
report_generator = ReportGenerator(manager)
data_generator = SyntheticDataGenerator()


def main():

    while True:

        print("\n" + "=" * 50)
        print("       PERSONAL EXPENSE TRACKER")
        print("=" * 50)

        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Expense Analytics")
        print("5. Data Visualization")
        print("6. Budget Management")
        print("7. Generate Reports")
        print("8. Generate Synthetic Data")
        print("9. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            manager.add_expense()

        elif choice == "2":
            manager.display_expenses()

        elif choice == "3":
            manager.delete_expense()

        elif choice == "4":
            analytics.display_analytics()

        elif choice == "5":
            visualizer.show_menu()

        elif choice == "6":
            budget_manager.show_menu()

        elif choice == "7":
            report_generator.show_menu()

        elif choice == "8":

            print("\n===== SYNTHETIC DATA GENERATOR =====")

            try:

                number = int(
                    input("How many demo records to generate? ")
                )

                if number <= 0:
                    print("Enter a number greater than zero.")
                    continue

                confirm = input(
                    f"Generate {number} records? (yes/no): "
                ).strip().lower()

                if confirm == "yes":

                    data_generator.save_data(
                        number_of_records=number,
                        replace_existing=False
                    )

                    print("\nSynthetic data generated successfully!")

                else:
                    print("Operation cancelled.")

            except ValueError:
                print("Please enter a valid number.")

            except Exception as error:
                print(f"Error: {error}")

        elif choice == "9":

            print("\nThank you for using Personal Expense Tracker!")
            print("Goodbye!")
            break

        else:
            print("\nInvalid choice! Please enter 1 to 9.")


if __name__ == "__main__":
    main()