# Validate menu choices, product IDs, quantities, and other inputs.

from datetime import datetime
from math import isfinite


def get_integer(message, minimum=1):
    while True:
        try:
            value = int(input(message).strip())

            if value >= minimum:
                return value

            print(f"Enter a whole number >= {minimum}.")

        except ValueError:
            print("Invalid input. Enter a whole number.")


def get_positive_number(message):
    while True:
        try:
            value = float(input(message).strip())

            if not isfinite(value) or value <= 0:
                print("Enter a finite number greater than zero.")
                continue

            return round(value, 2)

        except ValueError:
            print("Invalid input. Enter a valid number.")


def get_non_empty_text(message):
    while True:
        value = input(message).strip()

        if value:
            return value

        print("This field cannot be empty.")


def get_yes_no(message):
    while True:
        answer = input(message).strip().lower()

        if answer in ("y", "yes"):
            return True
        elif answer in ("n", "no"):
            return False
        else:
            print("Please enter Y or N.")


def get_date(message):
    while True:
        value = input(message).strip()

        try:
            return datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            print("Enter a valid date in DD-MM-YYYY format.")
