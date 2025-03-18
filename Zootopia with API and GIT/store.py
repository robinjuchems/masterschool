class Store:
    """A class representing a store that manages a list of products."""

    def __init__(self, products):
        """
        Initialize the store with a list of products.

        Args:
            products (list): A list of product objects to manage in the store.
        """
        self.products = products

    def get_total_quantity(self):
        """Return the total quantity of all products in the store."""
        return sum(product.get_quantity() for product in self.products)

    def get_all_products(self):
        """Return the list of all products in the store."""
        return self.products

    def order(self, shopping_list):
        """
        Process an order from a shopping list and return the total cost.

        Args:
            shopping_list (list): List of tuples (product, quantity) representing the order.

        Returns:
            float: Total cost of the order.

        Raises:
            ValueError: If any purchase fails (e.g., insufficient stock).
        """
        total_cost = 0
        for product, quantity in shopping_list:
            try:
                total_cost += product.buy(quantity)
            except ValueError as error:
                raise ValueError(f"Failed to order {product.name}: {error}") from error
        return total_cost

# Optional: Beispiel zur Verwendung (kann entfernt werden, wenn nicht benötigt)
if __name__ == "__main__":
    # Beispiel-Implementierung einer Product-Klasse zum Testen
    class Product:
        def __init__(self, name, price, quantity):
            self.name = name
            self.price = price
            self.quantity = quantity

        def get_quantity(self):
            return self.quantity

        def buy(self, quantity):
            if quantity > self.quantity:
                raise ValueError("Not enough stock")
            self.quantity -= quantity
            return self.price * quantity

        def __str__(self):
            return f"{self.name}: ${self.price}, Quantity: {self.quantity}"

    # Beispielprodukte
    products = [
        Product("Laptop", 1000, 5),
        Product("Phone", 500, 10)
    ]

    # Store-Instanz erstellen
    store = Store(products)

    # Test: Alle Produkte ausgeben
    print("All Products:")
    for product in store.get_all_products():
        print(product)

    # Test: Gesamtmenge
    print(f"Total Quantity: {store.get_total_quantity()}")

    # Test: Bestellung
    try:
        cost = store.order([(products[0], 2), (products[1], 3)])
        print(f"Order Total Cost: ${cost}")
    except ValueError as e:
        print(f"Order failed: {e}")