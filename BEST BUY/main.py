"""
Best Buy Store - Eine Webanwendung zur Verwaltung von Produkten im Laden.
"""

from products import Product
from store import Store


def show_menu() -> None:
    """Display the Best Buy store menu."""
    print("\n   Best Buy Store Menu")
    print("   ------------------")
    print("1. List all products in store")
    print("2. Show total quantity in store")
    print("3. Make an order")
    print("4. Quit")


def handle_order(store: Store) -> None:
    """Handle the process of making an order."""
    shopping_list = []
    print("Enter items to order (type 'done', 'finish', or 'exit' to finish):")
    while True:
        product_name = input("Enter product name (or 'done' to finish): ").strip()
        if product_name.lower() in ['done', 'finish', 'exit']:
            break
        try:
            quantity = float(input("Enter quantity: "))
            if quantity <= 0:
                print("Quantity must be positive.")
                continue
        except ValueError:
            print("Invalid quantity. Please enter a number.")
            continue
        product = next(
            (p for p in store.get_all_products() if p.name.lower() == product_name.lower()), None
        )
        if product:
            if product.is_active():
                shopping_list.append((product, quantity))
                print(f"Added {quantity:.2f} of {product_name} to your order.")
            else:
                print(f"{product_name} is out of stock.")
        else:
            print(f"Product '{product_name}' not found.")
    if shopping_list:
        try:
            total_cost = store.order(shopping_list)
            print(f"Order cost: ${total_cost:.2f}")
        except ValueError as error:
            print(f"Order failed: {error}")
    else:
        print("No items ordered.")


def main() -> None:
    """Initialize the store and run the main menu loop."""
    product_list = [
        Product("MacBook Air M2", price=1450.0, quantity=100.0),
        Product("Bose QuietComfort Earbuds", price=250.0, quantity=500.0),
        Product("Google Pixel 7", price=500.0, quantity=250.0),
    ]
    best_buy = Store(product_list)

    while True:
        show_menu()
        choice = input("Please choose a number: ").strip()
        if choice == "1":
            active_products = best_buy.get_all_products()
            if active_products:
                for product in active_products:
                    print(product.show())
            else:
                print("No active products available.")
        elif choice == "2":
            total_qty = best_buy.get_total_quantity()
            print(f"Total quantity in store: {total_qty:.2f}")
        elif choice == "3":
            handle_order(best_buy)
        elif choice == "4":
            print("Goodbye from Best Buy!")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
