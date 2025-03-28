"""
Modul für die Store-Klasse im Best Buy Store.
"""

class Store:
    """Eine Klasse, die einen Store mit einer Liste von Produkten repräsentiert."""

    def __init__(self, products: list) -> None:
        """Initialisiere den Store mit einer Liste von Produkten."""
        self.products = products

    def get_total_quantity(self) -> float:
        """Gibt die Gesamtmenge aller aktiven Produkte zurück."""
        return sum(product.get_quantity() for product in self.products if product.is_active())

    def get_all_products(self) -> list:
        """Gibt eine Liste aller aktiven Produkte zurück."""
        return [product for product in self.products if product.is_active()]

    def order(self, shopping_list: list) -> float:
        """Verarbeitet eine Bestellung und gibt die Gesamtkosten zurück.

        Args:
            shopping_list (list): Liste von Tupeln (Produkt, Menge).

        Returns:
            float: Gesamtkosten der Bestellung.

        Raises:
            ValueError: Wenn die Bestellung fehlschlägt (z. B. nicht genug Lagerbestand).
        """
        total_cost = 0.0
        for product, qty in shopping_list:
            total_cost += product.buy(float(qty))  # Sicherstellen, dass qty ein Float ist
        # Entferne Produkte, die nicht mehr aktiv sind
        self.products = [p for p in self.products if p.is_active()]
        return total_cost

    @staticmethod
    def get_store_description() -> str:
        """Gibt eine statische Beschreibung des Stores zurück."""
        return "Best Buy Store"

if __name__ == "__main__":
    from products import Product

    test_products = [
        Product("Test Laptop", 1000.0, 10.0),
        Product("Test Earbuds", 200.0, 5.0),
    ]
    test_store = Store(test_products)
    print(f"Gesamtmenge: {test_store.get_total_quantity():.2f}")
