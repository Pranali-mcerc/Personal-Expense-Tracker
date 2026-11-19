from datetime import datetime

CATEGORIES = [
    "Food",
    "Transportation",
    "Shopping",
    "Bills",
    "Education",
    "Healthcare",
    "Entertainment",
    "Travel",
    "Other"
]

PAYMENT_METHODS = [
    "UPI",
    "Cash",
    "Debit Card",
    "Credit Card",
    "Bank Transfer"
]


def validate_date(date_string):

    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d")

        if date_obj.date() > datetime.today().date():
            return False

        return True

    except ValueError:
        return False


def validate_amount(amount):

    try:
        amount = float(amount)

        return amount > 0

    except ValueError:
        return False


def validate_category(category):

    return category in CATEGORIES


def validate_payment_method(payment_method):

    return payment_method in PAYMENT_METHODS