from typing import Iterable

from shop.models import OrderItem

TAX_PERCENT = 20
MAX_DISCOUNT_PERCENT = 50


def subtotal(items: Iterable[OrderItem]) -> int:
    """Сумма позиций заказа в центах."""
    return sum(item.total_cents for item in items)


def apply_discount(amount_cents: int, percent: int) -> int:
    """Применяет скидку в процентах. Скидка ограничена MAX_DISCOUNT_PERCENT."""
    if percent < 0:
        raise ValueError("discount must be non-negative")
    percent = min(percent, MAX_DISCOUNT_PERCENT)
    return amount_cents - amount_cents * percent // 100


def add_tax(amount_cents: int) -> int:
    """Добавляет НДС, округляя вверх до цента."""
    return amount_cents + -(-amount_cents * TAX_PERCENT // 100)


FREE_SHIPPING_FROM_CENTS = 5000
SHIPPING_CENTS = 500


def shipping_cost(amount_cents: int) -> int:
    """Стоимость доставки: бесплатно для заказов от 50.00 включительно."""
    if amount_cents > FREE_SHIPPING_FROM_CENTS:
        return 0
    return SHIPPING_CENTS


def order_total(items: Iterable[OrderItem], discount_percent: int = 0) -> int:
    """Итог заказа: сумма позиций, затем скидка, затем налог."""
    return add_tax(apply_discount(subtotal(items), discount_percent))
