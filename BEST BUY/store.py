"""
Modul für die Store-Klasse im Best Buy Store.
"""


class Store:
    """A class representing a store with a list of products."""

    def __init__(self, products: list) -> None:
        """Initialize the store with a list of products."""
        self.products = products

    def get_total_quantity(self) -> float:
        """Return the total quantity of all products."""
        return sum(product.get_quantity() for product in self.products)

    def get_all_products(self) -> list:
        """Return a list of all active products."""
        return [product for product in self.products if product.is_active()]

    def order(self, shopping_list: list) -> float:
        """Process an order and return the total cost."""
        total_cost = 0.0
        for product, qty in shopping_list:
            total_cost += product.buy(qty)
        return total_cost

    @staticmethod
    def get_store_description() -> str:
        """Return a static description of the store."""
        return "Best Buy Store"


if __name__ == "__main__":
    from products import Product

    test_products = [
        Product("Test Laptop", 1000.0, 10.0),
        Product("Test Earbuds", 200.0, 5.0),
    ]
    test_store = Store(test_products)
    print(f"Total quantity: {test_store.get_total_quantity():.2f}")
