# Calculate daily expenditure and show previous bills for a selected date.

from modules.storage import load_bills
from modules.validation import get_date


def view_daily_expenditure():
    selected_date = get_date(
        "Enter date (DD-MM-YYYY): "
    ).strftime("%d-%m-%Y")

    bills = load_bills()

    daily_bills = [
        bill for bill in bills
        if bill.get("date_key") == selected_date
    ]

    print("\n" + "=" * 55)
    print("             DAILY EXPENDITURE REPORT")
    print("=" * 55)
    print("Date:", selected_date)
    print("-" * 55)

    if not daily_bills:
        print("No bills found for this date.")
        print("=" * 55)
        return

    total_spent = 0.0

    for bill in daily_bills:
        amount = bill["total"]
        total_spent += amount

        print("Bill No. :", bill["bill_number"])
        print("Customer :", bill["customer"])
        print(f"Amount   : Rs. {amount:.2f}")
        print("-" * 55)

    print("Number of bills:", len(daily_bills))
    print(f"Total expenditure: Rs. {total_spent:.2f}")
    print("=" * 55)
