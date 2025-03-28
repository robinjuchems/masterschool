"""
Modul für die Produktklasse im Best Buy Store.
"""

class Product:
    """Eine Klasse, die ein Produkt im Store repräsentiert."""

    def __init__(self, name: str, price: float, quantity: float) -> None:
        """Initialisiere ein Produkt mit Name, Preis und Menge."""
        if not name or price < 0 or quantity < 0:
            raise ValueError(
                "Ungültige Attribute: Name darf nicht leer sein, "
                "Preis und Menge müssen nicht-negativ sein."
            )
        self.name = name
        self.price = price
        self.quantity = float(quantity)  # Sicherstellen, dass es ein Float ist
        self._active = quantity > 0

    def get_quantity(self) -> float:
        """Gibt die aktuelle Menge des Produkts zurück."""
        return self.quantity

    def set_quantity(self, qty: float) -> None:
        """Setzt die Menge und aktualisiert den Aktivstatus."""
        if qty < 0:
            raise ValueError("Menge kann nicht negativ sein.")
        self.quantity = float(qty)
        self._active = qty > 0

    def is_active(self) -> bool:
        """Gibt zurück, ob das Produkt aktiv ist (hat Lagerbestand)."""
        return self._active

    def activate(self) -> None:
        """Aktiviert das Produkt, wenn es Lagerbestand hat."""
        if self.quantity > 0:
            self._active = True

    def deactivate(self) -> None:
        """Deaktiviert das Produkt."""
        self._active = False

    def buy(self, qty: float) -> float:
        """Kauft eine Menge und gibt die Kosten zurück."""
        if qty <= 0:
            raise ValueError("Kaufmenge muss größer als null sein.")
        if qty > self.quantity:
            raise ValueError(f"Nicht genug Lagerbestand für {self.name}. Verfügbar: {self.quantity}")
        self.quantity -= qty
        if self.quantity <= 0:  # Anpassung für Gleitkommazahlen
            self._active = False
        return qty * self.price

    def show(self) -> str:
        """Gibt eine formatierte Zeichenkette mit Produktdetails zurück."""
        return f"{self.name} - Preis: ${self.price:.2f}, Menge: {self.quantity:.2f}"

    def __str__(self) -> str:
        """Gibt eine Zeichenkettendarstellung des Produkts zurück."""
        return self.show()

if __name__ == "__main__":
    test_product = Product("Test Item", 10.0, 5.0)
    print(test_product.show())
