from typing import Iterable

from shop.models import OrderItem

TAX_PERCENT = 20
MAX_DISCOUNT = 0.5


def subtotal(items: Iterable[OrderItem]) -> int:
    """Сумма позиций заказа в центах."""
    return sum(item.total_cents for item in items)


def apply_discount(amount_cents: int, discount: float) -> int:
    """Применяет скидку, заданную долей (0.125 = 12.5%). Скидка ограничена MAX_DISCOUNT."""
    if discount < 0:
        raise ValueError("discount must be non-negative")
    discount = min(discount, MAX_DISCOUNT)
    return round(amount_cents * (1 - discount))


def add_tax(amount_cents: int) -> int:
    """Добавляет НДС, округляя вверх до цента."""
    return amount_cents + -(-amount_cents * TAX_PERCENT // 100)


def order_total(items: Iterable[OrderItem], discount: float = 0) -> int:
    """Итог заказа: сумма позиций, затем скидка, затем налог."""
    return add_tax(apply_discount(subtotal(items), discount))
