
from modules.storage import initialize_storage
from modules.products import show_products, add_product
from modules.billing import create_bill
from modules.expenditure import view_daily_expenditure


def main():
    try:
        initialize_storage()
    except (OSError, RuntimeError) as error:
        print(f"Unable to initialize storage: {error}")
        return

    while True:
        print("\nSMART BILLING & EXPENDITURE TRACKER\n")
        print("1. Create New Bill")
        print("2. View Product Catalogue")
        print("3. Add New Product")
        print("4. View Daily Expenditure")
        print("5. Exit")
        print("_" * 45)

        try:
            choice = input("Enter your choice (1-5): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("Application closed safely. Goodbye!")
            break

        if choice == "1":
            action = create_bill
        elif choice == "2":
            action = show_products
        elif choice == "3":
            action = add_product
        elif choice == "4":
            action = view_daily_expenditure
        elif choice == "5":
            print("Thank you for using Smart Billing!")
            print("Application closed successfully.")
            break
        else:
            print("Invalid choice! Enter a number from 1 to 5.")
            continue

        try:
            action()
        except (OSError, RuntimeError, ValueError, KeyError, TypeError) as error:
            print(f"\nUnable to complete this operation: {error}")
            print("Please check your input or data files and try again.")


if __name__ == "__main__":
    main()
