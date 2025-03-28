"""
Best Buy Store - Eine Webanwendung zur Verwaltung von Produkten im Laden.
"""

from products import Product
from store import Store

def show_menu() -> None:
    """Zeigt das Best Buy Store-Menü an."""
    print("\n   Best Buy Store Menu")
    print("   ------------------")
    print("1. List all products in store")
    print("2. Show total quantity in store")
    print("3. Make an order")
    print("4. Quit")

def handle_order(store: Store) -> None:
    """Verarbeitet den Prozess einer Bestellung."""
    shopping_list = []
    print("Gib Artikel zur Bestellung ein (tippe 'done', 'finish', oder 'exit' zum Beenden):")
    while True:
        product_name = input("Gib den Produktnamen ein (oder 'done' zum Beenden): ").strip()
        if product_name.lower() in ['done', 'finish', 'exit']:
            break
        try:
            quantity = float(input("Gib die Menge ein: "))
            if quantity <= 0:
                print("Menge muss positiv sein.")
                continue
        except ValueError:
            print("Ungültige Menge. Bitte gib eine Zahl ein.")
            continue
        product = next(
            (p for p in store.get_all_products() if p.name.lower() == product_name.lower()), None
        )
        if product:
            if product.is_active():
                shopping_list.append((product, quantity))
                print(f"{quantity:.2f} von {product_name} zur Bestellung hinzugefügt.")
            else:
                print(f"{product_name} ist ausverkauft.")
        else:
            print(f"Produkt '{product_name}' nicht gefunden.")
    if shopping_list:
        try:
            total_cost = store.order(shopping_list)
            print(f"Bestellkosten: ${total_cost:.2f}")
        except ValueError as error:
            print(f"Bestellung fehlgeschlagen: {error}")
    else:
        print("Keine Artikel bestellt.")

def main() -> None:
    """Initialisiere den Store und führe die Hauptschleife aus."""
    product_list = [
        Product("MacBook Air M2", price=1450.0, quantity=100.0),
        Product("Bose QuietComfort Earbuds", price=250.0, quantity=500.0),
        Product("Google Pixel 7", price=500.0, quantity=250.0),
    ]
    best_buy = Store(product_list)

    while True:
        show_menu()
        choice = input("Bitte wähle eine Nummer: ").strip()
        if choice == "1":
            active_products = best_buy.get_all_products()
            if active_products:
                for product in active_products:
                    print(product.show())
            else:
                print("Keine aktiven Produkte verfügbar.")
        elif choice == "2":
            total_qty = best_buy.get_total_quantity()
            print(f"Gesamtmenge im Store: {total_qty:.2f}")
        elif choice == "3":
            handle_order(best_buy)
        elif choice == "4":
            print("Auf Wiedersehen von Best Buy!")
            break
        else:
            print("Ungültige Wahl, bitte versuche es erneut.")

if __name__ == "__main__":
    main()
