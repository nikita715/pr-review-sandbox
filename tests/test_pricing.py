import unittest

from shop.models import OrderItem
from shop.pricing import add_tax, apply_discount, format_cents, order_total, subtotal


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

    def test_order_total(self):
        items = [OrderItem(1, 1, 1000)]
        self.assertEqual(order_total(items, 10), 1080)


    def test_format_cents(self):
        self.assertEqual(format_cents(0), "0.00")
        self.assertEqual(format_cents(5), "0.05")
        self.assertEqual(format_cents(1200), "12.00")
        self.assertEqual(format_cents(123456), "1234.56")

    def test_format_negative_rejected(self):
        with self.assertRaises(ValueError):
            format_cents(-1)


if __name__ == "__main__":
    unittest.main()
