import pytest
from products import Product

def test_create_normal_product():
    p = Product("MacBook Air M2", price=1450, quantity=100)
    assert p.name == "MacBook Air M2"
    assert p.price == 1450
    assert p.quantity == 100
    assert p.active is True

def test_create_product_invalid_empty_name():
    with pytest.raises(ValueError):
        Product("", price=1450, quantity=100)

def test_create_product_invalid_negative_price():
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-10, quantity=100)

def test_product_becomes_inactive_at_zero_quantity():
    p = Product("MacBook Air M2", price=1450, quantity=1)
    cost = p.buy(1)
    assert p.quantity == 0
    assert p.active is False
    assert cost == 1450

def test_product_purchase_modifies_quantity_and_returns_cost():
    p = Product("MacBook Air M2", price=1450, quantity=10)
    cost = p.buy(2)
    assert cost == 2 * 1450
    assert p.quantity == 8
    assert p.active is True

def test_buy_more_than_available_raises_exception():
    p = Product("MacBook Air M2", price=1450, quantity=5)
    with pytest.raises(ValueError):
        p.buy(10)
