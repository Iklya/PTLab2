
from django.test import TestCase

from shop.models import Customer, Product, Purchase


class ShopViewsTestCase(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            name="Ivanov Ivan",
            address="Svetlaya St."
        )

        self.product = Product.objects.create(
            name="Book",
            price=10000
        )

        self.product2 = Product.objects.create(
            name="Pen",
            price=1000
        )

    def test_index_accessibility(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_index_contains_products(self):
        response = self.client.get("/")

        self.assertContains(response, "Book")
        self.assertContains(response, "10000")

    def test_add_product_to_cart(self):
        response = self.client.post(
            f"/cart/add/{self.product.id}/"
        )

        self.assertRedirects(response, "/")

        session = self.client.session
        self.assertEqual(
            session["cart"],
            [self.product.id]
        )

    def test_add_multiple_products_to_cart(self):
        self.client.post(f"/cart/add/{self.product.id}/")
        self.client.post(f"/cart/add/{self.product2.id}/")

        self.assertEqual(
            self.client.session["cart"],
            [self.product.id, self.product2.id]
        )

    def test_remove_product_from_cart(self):
        self.client.post(f"/cart/add/{self.product.id}/")

        response = self.client.post("/cart/remove/0/")

        self.assertRedirects(response, "/")
        self.assertEqual(self.client.session["cart"], [])

    def test_cart_total(self):
        self.client.post(f"/cart/add/{self.product.id}/")
        self.client.post(f"/cart/add/{self.product2.id}/")

        response = self.client.get("/")

        self.assertEqual(response.context["cart_total"], 11000)
        self.assertEqual(response.context["discount_percent"], 5)
        self.assertEqual(response.context["final_total"], 10450)

    def test_purchase_page(self):
        self.client.post(f"/cart/add/{self.product.id}/")

        response = self.client.get("/buy/")

        self.assertEqual(response.status_code, 200)

    def test_purchase_creation(self):
        self.client.post(f"/cart/add/{self.product.id}/")
        self.client.post(f"/cart/add/{self.product2.id}/")

        response = self.client.post(
            "/buy/",
            {"customer": self.customer.id}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Purchase.objects.count(), 2)

        self.assertContains(response, "Ivanov Ivan")
        self.assertContains(response, "5%")
        self.assertContains(response, "10450")

    def test_cart_cleared_after_purchase(self):
        self.client.post(f"/cart/add/{self.product.id}/")

        self.client.post(
            "/buy/",
            {"customer": self.customer.id}
        )

        self.assertEqual(self.client.session["cart"], [])

    def test_old_purchases_do_not_affect_cart_discount(self):
        old_product = Product.objects.create(
            name="Old product",
            price=30000
        )

        Purchase.objects.create(
            customer=self.customer,
            product=old_product
        )

        self.client.post(f"/cart/add/{self.product2.id}/")

        response = self.client.get("/")

        self.assertEqual(response.context["cart_total"], 1000)
        self.assertEqual(response.context["discount_percent"], 0)

    def test_empty_cart_cannot_be_purchased(self):
        response = self.client.get("/buy/")

        self.assertRedirects(response, "/")

        self.assertEqual(Purchase.objects.count(), 0)
