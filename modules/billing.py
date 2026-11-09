
# Add multiple products, manage quantities, calculate discounts, GST, and final totals.

from datetime import datetime

from modules.storage import load_products, save_bill
from modules.validation import get_integer, get_non_empty_text

GST_RATE = 5.0


def get_discount_rate(subtotal):
    """Calculate the discount percentage based on the subtotal."""

    if subtotal >= 10000:
        return 15
    elif subtotal >= 5000:
        return 10
    elif subtotal >= 2000:
        return 5
    else:
        return 0


def show_selected_items(cart):
    """Display all items currently selected by the customer."""

    print("\n" + "=" * 55)
    print("                 YOUR SELECTED ITEMS")
    print("=" * 55)

    if not cart:
        print("No items selected yet.")
        return

    print(f"{'Product':<23}{'Qty':>6}{'Amount':>14}")
    print("-" * 55)

    for item in cart:
        print(
            f"{item['name'][:23]:<23}"
            f"{item['quantity']:>6}"
            f"{item['amount']:>14.2f}"
        )

    subtotal = round(sum(item["amount"] for item in cart), 2)

    print("-" * 55)
    print(f"{'Current subtotal:':<35} Rs. {subtotal:>10.2f}")
    print("=" * 55)


def print_receipt(bill):
    """Display the final bill receipt."""

    print("\n" + "=" * 62)
    print("             SMART BILLING SYSTEM")
    print("=" * 62)
    print("Bill Number :", bill["bill_number"])
    print("Customer    :", bill["customer"])
    print("Date        :", bill["date"])
    print("-" * 62)

    print(f"{'Product':<22}{'Qty':>6}{'Price':>14}{'Amount':>16}")
    print("-" * 62)

    for item in bill["items"]:
        print(
            f"{item['name'][:22]:<22}"
            f"{item['quantity']:>6}"
            f"{item['price']:>14.2f}"
            f"{item['amount']:>16.2f}"
        )

    print("-" * 62)
    print(f"{'Subtotal:':<42} Rs. {bill['subtotal']:>12.2f}")

    print(
        f"{'Discount (' + str(bill['discount_rate']) + '%):':<42}"
        f" Rs. {bill['discount_amount']:>12.2f}"
    )

    print(
        f"{'After discount:':<42}"
        f" Rs. {bill['taxable_amount']:>12.2f}"
    )

    print(
        f"{'GST (' + str(bill['gst_rate']) + '%):':<42}"
        f" Rs. {bill['gst_amount']:>12.2f}"
    )

    print("=" * 62)
    print(f"{'FINAL AMOUNT:':<42} Rs. {bill['total']:>12.2f}")
    print("=" * 62)
    print("              THANK YOU FOR SHOPPING!")
    print("=" * 62)


def create_bill():
    """Create a new bill with multiple products."""

    products = load_products()

    if not products:
        print("No products available. Please add products first.")
        return

    # Get customer information.
    customer = get_non_empty_text("Enter customer name: ")
    cart = []

    # Display the product catalogue only once.
    print("\n========== AVAILABLE PRODUCTS ==========")

    for product in products:
        print(
            f"{product['id']}. {product['name']}"
            f" - Rs. {product['price']:.2f}"
        )

    print("=" * 40)

    # Add products until the customer enters F.
    while True:
        choice = input(
            "\nEnter product ID or F to finish: "
        ).strip()

        # Finish billing.
        if choice.lower() == "f":
            if not cart:
                print("Please select at least one item before finishing.")
                continue

            break

        # Validate product ID input.
        try:
            product_id = int(choice)
        except ValueError:
            print("Invalid input. Enter a product ID or F to finish.")
            continue

        # Find the selected product.
        selected = None

        for product in products:
            if product["id"] == product_id:
                selected = product
                break

        if selected is None:
            print("Product not found. Please select a valid product ID.")
            continue

        # Get quantity.
        quantity = get_integer("Enter quantity: ")

        # Calculate the amount for this item.
        amount = round(selected["price"] * quantity, 2)

        # Add the item to the cart.
        cart.append({
            "product_id": selected["id"],
            "name": selected["name"],
            "price": selected["price"],
            "quantity": quantity,
            "amount": amount
        })

        # Confirm the added item without repeating the catalogue.
        print(
            f"\nAdded {selected['name']} x {quantity}"
            f" = Rs. {amount:.2f}"
        )

    # Calculate the subtotal.
    subtotal = round(
        sum(item["amount"] for item in cart),
        2
    )

    # Calculate discount.
    discount_rate = get_discount_rate(subtotal)
    discount_amount = round(
        subtotal * discount_rate / 100,
        2
    )

    # Calculate taxable amount after discount.
    taxable_amount = round(
        subtotal - discount_amount,
        2
    )

    # Calculate GST on the discounted amount.
    gst_amount = round(
        taxable_amount * GST_RATE / 100,
        2
    )

    # Calculate final payable amount.
    total = round(
        taxable_amount + gst_amount,
        2
    )

    # Prepare bill details.
    now = datetime.now()

    bill = {
        "bill_number": now.strftime("%Y%m%d%H%M%S%f"),
        "customer": customer,
        "date": now.strftime("%d-%m-%Y %H:%M:%S"),
        "date_key": now.strftime("%d-%m-%Y"),
        "items": cart,
        "subtotal": subtotal,
        "discount_rate": discount_rate,
        "discount_amount": discount_amount,
        "taxable_amount": taxable_amount,
        "gst_rate": GST_RATE,
        "gst_amount": gst_amount,
        "total": total
    }

    # Save the bill.
    try:
        save_bill(bill)

    except (OSError, RuntimeError) as error:
        print(f"\nUnable to save bill: {error}")
        print("The receipt will still be displayed, but it was not saved.")
        print_receipt(bill)
        return

    # Print the final receipt.
    print_receipt(bill)
    print("Bill saved successfully.")
