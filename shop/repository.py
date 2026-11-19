import sqlite3
from typing import List, Optional

from shop.models import Product

SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    id          INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL,
    price_cents INTEGER NOT NULL CHECK (price_cents >= 0),
    stock       INTEGER NOT NULL CHECK (stock >= 0)
);
"""


def connect(path: str = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.executescript(SCHEMA)
    return conn


class ProductRepository:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def add(self, name: str, price_cents: int, stock: int) -> Product:
        cur = self._conn.execute(
            "INSERT INTO products (name, price_cents, stock) VALUES (?, ?, ?)",
            (name, price_cents, stock),
        )
        self._conn.commit()
        return Product(cur.lastrowid, name, price_cents, stock)

    def get(self, product_id: int) -> Optional[Product]:
        row = self._conn.execute(
            "SELECT id, name, price_cents, stock FROM products WHERE id = ?",
            (product_id,),
        ).fetchone()
        return Product(*row) if row else None

    def search(self, query: str) -> List[Product]:
        rows = self._conn.execute(
            "SELECT id, name, price_cents, stock FROM products WHERE name LIKE ? ORDER BY name",
            (f"%{query}%",),
        ).fetchall()
        return [Product(*row) for row in rows]

    def list_in_stock(self) -> List[Product]:
        """Товары, которые есть в наличии, по алфавиту."""
        rows = self._conn.execute(
            "SELECT id, name, price_cents, stock FROM products WHERE stock > 0 ORDER BY name"
        ).fetchall()
        return [Product(*row) for row in rows]

    def reserve(self, product_id: int, quantity: int) -> bool:
        """Атомарно списывает остаток. Возвращает False, если товара не хватает."""
        cur = self._conn.execute(
            "UPDATE products SET stock = stock - ? WHERE id = ? AND stock >= ?",
            (quantity, product_id, quantity),
        )
        return cur.rowcount == 1
