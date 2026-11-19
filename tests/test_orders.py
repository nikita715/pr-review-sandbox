import unittest

from shop.orders import OrderError, OrderService
from shop.repository import ProductRepository, connect


class OrderServiceTest(unittest.TestCase):
    def setUp(self):
        self.repo = ProductRepository(connect())
        self.book = self.repo.add("Book", 1000, 5)
        self.pen = self.repo.add("Pen", 150, 1)
        self.service = OrderService(self.repo)

    def test_create_order(self):
        order = self.service.create_order({self.book.id: 2, self.pen.id: 1})
        self.assertEqual(order.total_cents, 2580)  # (2000 + 150) * 1.2
        self.assertEqual(self.repo.get(self.book.id).stock, 3)
        self.assertEqual(self.repo.get(self.pen.id).stock, 0)

    def test_not_enough_stock_reserves_nothing(self):
        with self.assertRaises(OrderError):
            self.service.create_order({self.book.id: 1, self.pen.id: 2})
        self.assertEqual(self.repo.get(self.book.id).stock, 5)

    def test_create_order_by_names(self):
        order = self.service.create_order_by_names({"Book": 2, "Pen": 1})
        self.assertEqual(order.total_cents, 2580)
        self.assertEqual(self.repo.get(self.book.id).stock, 3)

    def test_unknown_product(self):
        with self.assertRaises(OrderError):
            self.service.create_order({999: 1})

    def test_empty_order(self):
        with self.assertRaises(OrderError):
            self.service.create_order({})

    def test_search(self):
        self.assertEqual([p.name for p in self.repo.search("oo")], ["Book"])


if __name__ == "__main__":
    unittest.main()
