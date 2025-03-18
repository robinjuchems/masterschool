class Product:
    """A class representing a product in the store with name, price, and quantity."""

    def __init__(self, name: str, price: float, quantity: int):
        if not name or price < 0 or quantity < 0:
            raise ValueError(
                "Invalid product attributes: name cannot be empty, "
                "price and quantity must be non-negative."
            )
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = quantity > 0

    def get_quantity(self) -> int:
        """Return the current quantity of the product."""
        return self.quantity

    def is_active(self) -> bool:
        """Return whether the product is active (has stock)."""
        return self.active

    def buy(self, quantity: int) -> float:
        """Purchase a specified quantity of the product and return the cost."""
        if quantity <= 0:
            raise ValueError("Purchase quantity must be greater than zero.")
        if quantity > self.quantity:
            raise ValueError(
                f"Not enough stock for {self.name}. "
                f"Available: {self.quantity}, Requested: {quantity}"
            )
        self.quantity -= quantity
        if self.quantity == 0:
            self.active = False
        return quantity * self.price

    def show(self) -> str:
        """Return a formatted string with product details."""
        return f"{self.name} - Price: ${self.price:.2f}, Quantity: {self.quantity}"
