from django.test import TestCase

from shop.models import Customer, Product, Purchase


class ProductTestCase(TestCase):
    def setUp(self):
        self.book = Product.objects.create(
            name="book",
            price=740
        )
        self.pencil = Product.objects.create(
            name="pencil",
            price=50
        )

    def test_product_creation(self):
        self.assertEqual(Product.objects.count(), 2)

    def test_product_data(self):
        self.assertEqual(self.book.name, "book")
        self.assertEqual(self.book.price, 740)
        self.assertEqual(self.pencil.name, "pencil")
        self.assertEqual(self.pencil.price, 50)

    def test_product_types(self):
        self.assertIsInstance(self.book.name, str)
        self.assertIsInstance(self.book.price, int)

    def test_product_string_representation(self):
        self.assertEqual(str(self.book), "book")


class CustomerTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Ivanov Ivan",
            address="Svetlaya St."
        )

    def test_customer_creation(self):
        self.assertEqual(Customer.objects.count(), 1)

    def test_customer_data(self):
        self.assertEqual(self.customer.name, "Ivanov Ivan")
        self.assertEqual(
            self.customer.address,
            "Svetlaya St."
        )

    def test_customer_string_representation(self):
        self.assertEqual(str(self.customer), "Ivanov Ivan")

    def test_customer_has_no_purchases(self):
        self.assertEqual(self.customer.purchases.count(), 0)

    def test_zero_total_spent(self):
        self.assertEqual(self.customer.total_spent(), 0)

    def test_zero_discount(self):
        self.assertEqual(self.customer.discount_percent(), 0)

    def test_zero_discount_amount(self):
        self.assertEqual(self.customer.discount_amount(), 0)

    def test_zero_total_with_discount(self):
        self.assertEqual(self.customer.total_with_discount(), 0)


class PurchaseTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Ivanov Ivan",
            address="Svetlaya St."
        )

        self.book = Product.objects.create(
            name="book",
            price=740
        )

        self.purchase = Purchase.objects.create(
            customer=self.customer,
            product=self.book
        )

    def test_purchase_creation(self):
        self.assertEqual(Purchase.objects.count(), 1)

    def test_purchase_customer(self):
        self.assertEqual(
            self.purchase.customer,
            self.customer
        )

    def test_purchase_product(self):
        self.assertEqual(
            self.purchase.product,
            self.book
        )

    def test_purchase_date_exists(self):
        self.assertIsNotNone(self.purchase.date)

    def test_purchase_string_representation(self):
        self.assertEqual(
            str(self.purchase),
            "Ivanov Ivan: book"
        )

    def test_purchase_is_added_to_customer(self):
        self.assertEqual(
            self.customer.purchases.count(),
            1
        )

    def test_total_spent(self):
        self.assertEqual(
            self.customer.total_spent(),
            740
        )


class DiscountTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Ivanov Ivan",
            address="Svetlaya St."
        )

    def add_product(self, name, price):
        product = Product.objects.create(
            name=name,
            price=price
        )

        Purchase.objects.create(
            customer=self.customer,
            product=product
        )

    def test_discount_below_5000(self):
        self.add_product("Product", 4999)

        self.assertEqual(
            self.customer.total_spent(),
            4999
        )
        self.assertEqual(
            self.customer.discount_percent(),
            0
        )

    def test_discount_from_5000(self):
        self.add_product("Product", 5000)

        self.assertEqual(
            self.customer.discount_percent(),
            3
        )

    def test_discount_from_10000(self):
        self.add_product("Product", 10000)

        self.assertEqual(
            self.customer.discount_percent(),
            5
        )

    def test_discount_from_20000(self):
        self.add_product("Product", 20000)

        self.assertEqual(
            self.customer.discount_percent(),
            10
        )

    def test_discount_amount(self):
        self.add_product("Product", 10000)

        self.assertEqual(
            self.customer.discount_amount(),
            500
        )

    def test_total_with_discount(self):
        self.add_product("Product", 10000)

        self.assertEqual(
            self.customer.total_with_discount(),
            9500
        )

    def test_six_products(self):
        prices = [1000, 2000, 1500, 3000, 500, 2000]

        for number, price in enumerate(prices):
            self.add_product(
                f"Product {number + 1}",
                price
            )

        self.assertEqual(
            self.customer.purchases.count(),
            6
        )

        self.assertEqual(
            self.customer.total_spent(),
            10000
        )

        self.assertEqual(
            self.customer.discount_percent(),
            5
        )

        self.assertEqual(
            self.customer.discount_amount(),
            500
        )

        self.assertEqual(
            self.customer.total_with_discount(),
            9500
        )

    def test_customers_have_independent_discounts(self):
        second_customer = Customer.objects.create(
            name="Petrov Petr",
            address="Lenina St."
        )

        self.add_product("Product 1", 10000)

        product = Product.objects.create(
            name="Product 2",
            price=1000
        )

        Purchase.objects.create(
            customer=second_customer,
            product=product
        )

        self.assertEqual(
            self.customer.discount_percent(),
            5
        )

        self.assertEqual(
            second_customer.discount_percent(),
            0
        )
