# Display products and manage the product catalogue.

from modules.storage import load_products, save_products
from modules.validation import get_non_empty_text, get_positive_number


def show_products():
    products = load_products()

    print("\n========== PRODUCT CATALOGUE ==========")
    print(f"{'ID':<6}{'Product':<24}{'Price (Rs.)':>12}")
    print("-" * 42)

    if not products:
        print("No products available.")
        return

    for product in products:
        print(
            f"{product['id']:<6}"
            f"{product['name']:<24}"
            f"{product['price']:>12.2f}"
        )

    print("-" * 42)


def add_product():
    products = load_products()

    name = get_non_empty_text("Enter product name: ")

    for product in products:
        if product["name"].casefold() == name.casefold():
            print("This product already exists.")
            return

    price = get_positive_number("Enter product price: ")

    if products:
        new_id = max(product["id"] for product in products) + 1
    else:
        new_id = 1

    products.append({
        "id": new_id,
        "name": name,
        "price": price
    })

    save_products(products)
    print(f"Product '{name}' added successfully.")
