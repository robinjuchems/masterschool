class Product:
    """A class representing a standard product in the store."""

    def __init__(self, name: str, price: float, quantity: int):
        """Initialize a product with name, price, and quantity."""
        if not name or price < 0 or quantity < 0:
            raise ValueError("Invalid product attributes: name cannot be empty, price and quantity must be non-negative.")
        self.name = name
        self.price = price
        self.quantity = quantity
        self.promotion = None
        self.active = quantity > 0  # Für Tests angepasst

    def get_quantity(self) -> int:
        """Return the current quantity of the product."""
        return self.quantity

    def buy(self, quantity: int) -> float:
        """Purchase a quantity of the product and return the cost."""
        if quantity <= 0:
            raise ValueError("Purchase quantity must be greater than zero.")
        if quantity > self.quantity:
            raise ValueError(f"Not enough stock for {self.name}. Available: {self.quantity}")
        self.quantity -= quantity
        if self.quantity == 0:
            self.active = False  # Für Tests angepasst
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return quantity * self.price

    def __str__(self) -> str:
        """Return a string representation of the product."""
        promo = f" (Promotion: {self.promotion.name})" if self.promotion else ""
        return f"{self.name} - Price: ${self.price:.2f}, Quantity: {self.quantity}{promo}"

    def __gt__(self, other) -> bool:
        """Compare products by price."""
        return self.price > other.price

    def __eq__(self, other) -> bool:
        """Check if two products are equal by name."""
        return self.name == other.name


class NonStockedProduct(Product):
    """A class representing a product with unlimited stock."""

    def __init__(self, name: str, price: float):
        """Initialize a non-stocked product with unlimited quantity."""
        super().__init__(name, price, quantity=0)

    def get_quantity(self) -> int:
        """Return infinity for non-stocked products."""
        return float('inf')

    def buy(self, quantity: int) -> float:
        """Purchase a quantity without affecting stock."""
        if quantity <= 0:
            raise ValueError("Purchase quantity must be greater than zero.")
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return quantity * self.price


class LimitedProduct(Product):
    """A class representing a product with a purchase limit per order."""

    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        """Initialize a limited product with a maximum purchase limit."""
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def buy(self, quantity: int) -> float:
        """Purchase a quantity with a maximum limit per order."""
        if quantity <= 0:
            raise ValueError("Purchase quantity must be greater than zero.")
        if quantity > self.maximum:
            raise ValueError(f"Cannot order more than {self.maximum} of {self.name} per order.")
        if quantity > self.quantity:
            raise ValueError(f"Not enough stock for {self.name}. Available: {self.quantity}")
        self.quantity -= quantity
        if self.quantity == 0:
            self.active = False
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return quantity * self.price

