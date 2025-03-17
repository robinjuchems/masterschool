class Store:
    """A class representing a store that manages a list of products."""

    def __init__(self, products):
        self.products = products

    def get_total_quantity(self):
        """Return the total quantity of all products in the store."""
        return sum(product.get_quantity() for product in self.products)

    @staticmethod
    def get_all_products(self):
        """Return the list of all products in the store."""
        return self.products

    def order(self, shopping_list):
        """
        Process an order from a shopping list and return the total cost.

        Args:
            shopping_list: List of tuples (product, quantity)

        Raises:
            ValueError: If any purchase fails (e.g., insufficient stock)
        """
        total_cost = 0
        for product, quantity in shopping_list:
            try:
                total_cost += product.buy(quantity)
            except ValueError as error:
                raise ValueError(f"Failed to order {product.name}: {error}") from error
        return total_cost
