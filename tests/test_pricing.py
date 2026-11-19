import unittest

from shop.models import OrderItem
from shop.pricing import add_tax, apply_discount, order_total, subtotal


class PricingTest(unittest.TestCase):
    def test_subtotal(self):
        items = [OrderItem(1, 2, 150), OrderItem(2, 1, 1000)]
        self.assertEqual(subtotal(items), 1300)

    def test_discount(self):
        self.assertEqual(apply_discount(1000, 0.1), 900)

    def test_fractional_discount(self):
        self.assertEqual(apply_discount(1000, 0.125), 875)

    def test_discount_is_capped(self):
        self.assertEqual(apply_discount(1000, 0.9), 500)

    def test_negative_discount_rejected(self):
        with self.assertRaises(ValueError):
            apply_discount(1000, -0.05)

    def test_tax_rounds_up(self):
        self.assertEqual(add_tax(1000), 1200)
        self.assertEqual(add_tax(1), 2)

    def test_order_total(self):
        items = [OrderItem(1, 1, 1000)]
        self.assertEqual(order_total(items, 0.1), 1080)


if __name__ == "__main__":
    unittest.main()
