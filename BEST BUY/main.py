from products import Product
from store import Store

def show_menu():
    """Display the Best Buy store menu options."""
    print("\n   Best Buy Store Menu")
    print("   ------------------")
    print("1. List all products in store")
    print("2. Show total quantity in store")
    print("3. Make an order")
    print("4. Quit")

def handle_order(store):
    """Handle the process of making an order from the store."""
    shopping_list = []
    print("Enter items to order (type 'done' to finish):")
    while True:
        product_name = input("Product name: ")
        if product_name.lower() == 'done':
            break
        try:
            quantity = int(input("Enter quantity: "))
            if quantity <= 0:
                print("Quantity must be positive.")
                continue
        except ValueError:
            print("Invalid quantity.")
            continue
        product = next((p for p in store.get_all_products() if p.name == product_name), None)
        if product:
            shopping_list.append((product, quantity))
        else:
            print("Product not found.")
    if shopping_list:
        try:
            total_cost = store.order(shopping_list)
            print(f"Order placed! Total cost: ${total_cost:.2f}")
        except ValueError as error:
            print(f"Order failed: {error}")
    else:
        print("No items ordered.")

def main():
    """Initialize the store and run the main menu loop."""
    # Setup initial stock of inventory
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250)
    ]
    best_buy = Store(product_list)

    while True:
        show_menu()
        choice = input("Please choose a number: ")
        if choice == "1":
            for product in best_buy.get_all_products():
                print(product.show())
        elif choice == "2":
            print(f"Total quantity in store: {best_buy.get_total_quantity()}")
        elif choice == "3":
            handle_order(best_buy)
        elif choice == "4":
            print("Goodbye from Best Buy!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
