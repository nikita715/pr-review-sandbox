import unittest

from shop.models import OrderItem
from shop.pricing import add_tax, apply_discount, order_total, shipping_cost, subtotal


class PricingTest(unittest.TestCase):
    def test_subtotal(self):
        items = [OrderItem(1, 2, 150), OrderItem(2, 1, 1000)]
        self.assertEqual(subtotal(items), 1300)

    def test_discount(self):
        self.assertEqual(apply_discount(1000, 10), 900)

    def test_discount_is_capped(self):
        self.assertEqual(apply_discount(1000, 90), 500)

    def test_negative_discount_rejected(self):
        with self.assertRaises(ValueError):
            apply_discount(1000, -5)

    def test_tax_rounds_up(self):
        self.assertEqual(add_tax(1000), 1200)
        self.assertEqual(add_tax(1), 2)

    def test_shipping_cost(self):
        self.assertEqual(shipping_cost(1000), 500)
        self.assertEqual(shipping_cost(7500), 0)

    def test_order_total(self):
        items = [OrderItem(1, 1, 1000)]
        self.assertEqual(order_total(items, 10), 1080)


if __name__ == "__main__":
    unittest.main()
