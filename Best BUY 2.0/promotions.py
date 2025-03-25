from abc import ABC, abstractmethod

class Promotion(ABC):
    """Abstract base class for promotions."""

    def __init__(self, name: str):
        """Initialize a promotion with a name."""
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity: int) -> float:
        """Apply the promotion to a product purchase."""
        pass


class PercentDiscount(Promotion):
    """A promotion that applies a percentage discount."""

    def __init__(self, name: str, percent: float):
        """Initialize with a name and discount percentage."""
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity: int) -> float:
        """Apply a percentage discount to the total cost."""
        full_price = product.price * quantity
        discount = full_price * (self.percent / 100)
        return full_price - discount


class SecondHalfPrice(Promotion):
    """A promotion where the second item is half price."""

    def apply_promotion(self, product, quantity: int) -> float:
        """Apply half price to every second item."""
        full_price_pairs = (quantity // 2) * (product.price + product.price * 0.5)
        remaining_items = (quantity % 2) * product.price
        return full_price_pairs + remaining_items


class ThirdOneFree(Promotion):
    """A promotion where every third item is free."""

    def apply_promotion(self, product, quantity: int) -> float:
        """Apply a free item for every third purchase."""
        sets_of_three = quantity // 3
        paid_items = quantity - sets_of_three
        return paid_items * product.price