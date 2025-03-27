"""
Modul für die Produktklasse im Best Buy Store.
"""


class Product:
    """A class representing a product in the store."""

    def __init__(self, name: str, price: float, quantity: float) -> None:
        """Initialize a product with name, price, and quantity."""
        if not name or price < 0 or quantity < 0:
            raise ValueError(
                "Invalid attributes: name must not be empty, "
                "price and quantity must be non-negative."
            )
        self.name = name
        self.price = price
        self.quantity = quantity
        self._active = quantity > 0

    def get_quantity(self) -> float:
        """Return the current quantity of the product."""
        return self.quantity

    def set_quantity(self, qty: float) -> None:
        """Set the quantity and update active status."""
        if qty < 0:
            raise ValueError("Quantity cannot be negative.")
        self.quantity = qty
        self._active = qty > 0

    def is_active(self) -> bool:
        """Return whether the product is active (has stock)."""
        return self._active

    def activate(self) -> None:
        """Activate the product if it has stock."""
        if self.quantity > 0:
            self._active = True

    def deactivate(self) -> None:
        """Deactivate the product."""
        self._active = False

    def buy(self, qty: float) -> float:
        """Purchase a quantity and return the cost."""
        if qty <= 0:
            raise ValueError("Purchase quantity must be greater than zero.")
        if qty > self.quantity:
            raise ValueError(f"Not enough stock for {self.name}. Available: {self.quantity}")
        self.quantity -= qty
        if self.quantity == 0:
            self._active = False
        return qty * self.price

    def show(self) -> str:
        """Return a formatted string with product details."""
        return f"{self.name} - Price: ${self.price:.2f}, Quantity: {self.quantity:.2f}"

    def __str__(self) -> str:
        """Return a string representation of the product."""
        return self.show()


if __name__ == "__main__":
    test_product = Product("Test Item", 10.0, 5.0)
    print(test_product.show())
