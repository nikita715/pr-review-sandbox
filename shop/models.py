from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class Product:
    id: int
    name: str
    price_cents: int
    stock: int


@dataclass(frozen=True)
class OrderItem:
    product_id: int
    quantity: int
    unit_price_cents: int

    @property
    def total_cents(self) -> int:
        return self.unit_price_cents * self.quantity


@dataclass
class Order:
    id: int
    items: List[OrderItem] = field(default_factory=list)
    discount_percent: int = 0
    tax_cents: int = 0
    total_cents: int = 0
