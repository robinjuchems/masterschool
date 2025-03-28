from products import Product, NonStockedProduct, LimitedProduct
from promotions import PercentDiscount, SecondHalfPrice, ThirdOneFree
from store import Store

def show_menu():
    """Display the Best Buy store menu."""
    print("\n   Best Buy 2.0 Store Menu")
    print("   ----------------------")
    print("1. List all products in store")
    print("2. Show total quantity in store")
    print("3. Make an order")
    print("4. Quit")

def handle_order(store):
    """Handle the process of making an order."""
    shopping_list = []
    print("Enter items to order (type 'done' to finish):")
    while True:
        product_name = input("Enter product name (or 'done' to finish): ").strip()
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
        product = next((p for p in store.get_all_products() if p.name.lower() == product_name.lower()), None)
        if product:
            shopping_list.append((product, quantity))
        else:
            print(f"Product not found. You entered: '{product_name}'")
    if shopping_list:
        try:
            total_cost = store.order(shopping_list)
            print(f"Order placed! Total cost: ${total_cost:.2f}")
        except ValueError as error:
            print(f"Order failed: {error}")
    else:
        print("No items ordered.")

def main():
    """Initialize and run the Best Buy 2.0 store with all features."""
    # Setup initial stock of inventory (Schritt 3)
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),  # Schritt 2
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1)  # Schritt 2
    ]

    # Create promotion catalog (Schritt 3)
    second_half_price = SecondHalfPrice("Second Half Price!")
    third_one_free = ThirdOneFree("Third One Free!")
    thirty_percent = PercentDiscount("30% off!", percent=30)

    # Add promotions to products (Schritt 3)
    product_list[0].promotion = second_half_price
    product_list[1].promotion = third_one_free
    product_list[3].promotion = thirty_percent

    best_buy = Store(product_list)

    # Bonus-Schritt: Magic Methods Tests
    print("\nBonus Tests:")
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    pixel = Product("Google Pixel 7", price=500, quantity=250)
    try:
        mac.price = -100  # Sollte Fehler auslösen
    except ValueError as e:
        print(f"Error setting negative price: {e}")
    print(mac)  # Nutzt __str__
    print(f"mac > bose: {mac > bose}")  # True
    print(f"mac in best_buy: {mac in best_buy}")  # False (neues Objekt)
    print(f"pixel in best_buy: {pixel in best_buy}")  # False (neues Objekt)

    store1 = Store([mac, bose])
    store2 = Store([pixel])
    combined_store = store1 + store2
    print(f"Combined store products: {len(combined_store.get_all_products())}")

    while True:
        show_menu()
        choice = input("Please choose a number: ")
        if choice == "1":
            print("Available products:")
            for product in best_buy.get_all_products():
                print(product)
        elif choice == "2":
            print(f"Total quantity in store: {best_buy.get_total_quantity()}")
        elif choice == "3":
            handle_order(best_buy)
        elif choice == "4":
            print("Goodbye from Best Buy 2.0!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()