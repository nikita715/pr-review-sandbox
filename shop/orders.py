import itertools
from typing import Dict

from shop.models import Order, OrderItem
from shop.pricing import order_total
from shop.repository import ProductRepository


class OrderError(Exception):
    pass


class OrderService:
    def __init__(self, products: ProductRepository):
        self._products = products
        self._ids = itertools.count(1)

    def create_order(self, quantities: Dict[int, int], discount_percent: int = 0) -> Order:
        """Создаёт заказ из {product_id: quantity} и резервирует товар.

        Если хотя бы одной позиции не хватает, ничего не резервируется.
        """
        if not quantities:
            raise OrderError("order is empty")

        # Сначала проверяем все позиции, чтобы не трогать БД для заведомо невалидного заказа
        products = {}
        for product_id, quantity in quantities.items():
            if quantity <= 0:
                raise OrderError(f"invalid quantity for product {product_id}")
            product = self._products.get(product_id)
            if product is None:
                raise OrderError(f"product {product_id} not found")
            if product.stock < quantity:
                raise OrderError(f"not enough stock for product {product_id}")
            products[product_id] = product

        items = []
        for product_id, quantity in quantities.items():
            if not self._products.reserve(product_id, quantity):
                raise OrderError(f"not enough stock for product {product_id}")
            items.append(OrderItem(product_id, quantity, products[product_id].price_cents))
        self._products._conn.commit()

        return Order(
            id=next(self._ids),
            items=items,
            discount_percent=discount_percent,
            total_cents=order_total(items, discount_percent),
        )
