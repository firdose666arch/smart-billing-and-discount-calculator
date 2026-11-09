
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

PRODUCT_FILE = DATA_DIR / "products.json"
BILL_FILE = DATA_DIR / "bills.json"

DEFAULT_PRODUCTS = [
    {"id": 1, "name": "Keyboard", "price": 800.00},
    {"id": 2, "name": "Mouse", "price": 500.00},
    {"id": 3, "name": "Monitor", "price": 7500.00},
    {"id": 4, "name": "USB Cable", "price": 150.00},
    {"id": 5, "name": "Headphones", "price": 1200.00}
]


def save_json(file_path, data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_json(file_path, default):
    if not file_path.exists():
        return default.copy() if isinstance(default, list) else default

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()

            if not content:
                return default.copy() if isinstance(default, list) else default

            return json.loads(content)

    except json.JSONDecodeError:
        print(
            f"Warning: {file_path.name} is invalid. "
            "Restoring default data."
        )
        return default.copy() if isinstance(default, list) else default

    except OSError as error:
        raise RuntimeError(
            f"Cannot read {file_path.name}: {error}"
        ) from error


def initialize_storage():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Restore missing, empty, or invalid product data.
    products = load_json(PRODUCT_FILE, DEFAULT_PRODUCTS)

    if not isinstance(products, list) or not products:
        products = DEFAULT_PRODUCTS.copy()

    save_json(PRODUCT_FILE, products)

    # Restore missing or invalid bill history.
    bills = load_json(BILL_FILE, [])

    if not isinstance(bills, list):
        bills = []

    save_json(BILL_FILE, bills)


def load_products():
    products = load_json(PRODUCT_FILE, DEFAULT_PRODUCTS)

    if not isinstance(products, list) or not products:
        products = DEFAULT_PRODUCTS.copy()
        save_json(PRODUCT_FILE, products)

    return products


def save_products(products):
    save_json(PRODUCT_FILE, products)


def load_bills():
    bills = load_json(BILL_FILE, [])

    if not isinstance(bills, list):
        return []

    return bills


def save_bill(bill):
    bills = load_bills()
    bills.append(bill)
    save_json(BILL_FILE, bills)
