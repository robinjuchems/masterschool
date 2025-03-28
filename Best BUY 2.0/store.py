class Store:
    """A class managing a collection of products."""

    def __init__(self, products):
        """Initialize the store with a list of products."""
        self.products = products

    def get_total_quantity(self) -> int:
        """Return the total quantity of all products."""
        return sum(product.get_quantity() for product in self.products)

    def get_all_products(self):
        """Return the list of all products."""
        return self.products

    def order(self, shopping_list) -> float:
        """Process an order and return the total cost."""
        total_cost = 0
        for product, quantity in shopping_list:
            total_cost += product.buy(quantity)
        return total_cost

    def __contains__(self, product) -> bool:
        """Check if a product is in the store."""
        return any(p == product for p in self.products)

    def __add__(self, other):
        """Combine two stores into a new store."""
        return Store(self.products + other.products)