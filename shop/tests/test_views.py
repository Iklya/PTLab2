from django.test import TestCase, Client

from shop.models import Customer, Product, Purchase


class ShopViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.product = Product.objects.create(
            name="book",
            price=10000
        )

        self.customer = Customer.objects.create(
            name="Ivanov Ivan",
            address="Svetlaya St."
        )

    def test_index_accessibility(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)

    def test_index_contains_product(self):
        response = self.client.get('/')

        self.assertContains(response, "book")
        self.assertContains(response, "10000")

    def test_customer_add_page_accessibility(self):
        response = self.client.get('/customer/add/')

        self.assertEqual(response.status_code, 200)

    def test_customer_creation(self):
        response = self.client.post(
            '/customer/add/',
            {
                'name': 'Petrov Petr',
                'address': 'Lenina St.'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Customer.objects.filter(
                name='Petrov Petr'
            ).exists()
        )

    def test_purchase_page_accessibility(self):
        response = self.client.get('/buy/')

        self.assertEqual(response.status_code, 200)

    def test_purchase_creation(self):
        response = self.client.post(
            '/buy/',
            {
                'customer': self.customer.id,
                'product': self.product.id
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            Purchase.objects.count(),
            1
        )

        self.assertContains(
            response,
            "Ivanov Ivan"
        )

    def test_purchase_response_contains_discount(self):
        response = self.client.post(
            '/buy/',
            {
                'customer': self.customer.id,
                'product': self.product.id
            }
        )

        self.assertContains(
            response,
            "5%"
        )

        self.assertContains(
            response,
            "9500"
        )