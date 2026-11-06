
from django.test import TestCase

from shop.models import Customer, Product, Purchase
from shop.views import calculate_discount


class ProductTestCase(TestCase):

    def test_product_creation(self):
        product = Product.objects.create(
            name="Book",
            price=1000
        )

        self.assertEqual(product.name, "Book")
        self.assertEqual(product.price, 1000)
        self.assertEqual(str(product), "Book")


class CustomerTestCase(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            name="Ivanov Ivan",
            address="Svetlaya St."
        )

    def test_customer_creation(self):
        self.assertEqual(Customer.objects.count(), 1)

    def test_customer_without_purchases(self):
        self.assertEqual(self.customer.total_spent(), 0)

    def test_customer_total_spent(self):
        product1 = Product.objects.create(
            name="Book",
            price=3000
        )
        product2 = Product.objects.create(
            name="Pen",
            price=2000
        )

        Purchase.objects.create(
            customer=self.customer,
            product=product1
        )
        Purchase.objects.create(
            customer=self.customer,
            product=product2
        )

        self.assertEqual(self.customer.total_spent(), 5000)


class DiscountTestCase(TestCase):

    def test_discount_below_5000(self):
        self.assertEqual(calculate_discount(4999), 0)

    def test_discount_at_5000(self):
        self.assertEqual(calculate_discount(5000), 3)

    def test_discount_at_10000(self):
        self.assertEqual(calculate_discount(10000), 5)

    def test_discount_at_20000(self):
        self.assertEqual(calculate_discount(20000), 10)

    def test_discount_between_5000_and_10000(self):
        self.assertEqual(calculate_discount(7500), 3)

    def test_discount_between_10000_and_20000(self):
        self.assertEqual(calculate_discount(15000), 5)

    def test_zero_cart(self):
        self.assertEqual(calculate_discount(0), 0)

    def test_discount_does_not_depend_on_customer_history(self):
        customer = Customer.objects.create(
            name="Petrov Petr",
            address="Lenina St."
        )

        old_product = Product.objects.create(
            name="Old purchase",
            price=30000
        )

        Purchase.objects.create(
            customer=customer,
            product=old_product
        )

        self.assertEqual(calculate_discount(1000), 0)
        self.assertEqual(calculate_discount(6000), 3)

    def test_discount_amount(self):
        total = 10000
        discount = calculate_discount(total)

        self.assertEqual(total * discount // 100, 500)

    def test_final_total(self):
        total = 10000
        discount = calculate_discount(total)
        discount_amount = total * discount // 100

        self.assertEqual(total - discount_amount, 9500)
