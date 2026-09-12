from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def total_spent(self):
        return sum(purchase.product.price for purchase in self.purchases.select_related('product').all())

    def discount_percent(self):
        total = self.total_spent()

        if total >= 20000:
            return 10
        if total >= 10000:
            return 5
        if total >= 5000:
            return 3

        return 0

    def discount_amount(self):
        return self.total_spent() * self.discount_percent() / 100

    def total_with_discount(self):
        return self.total_spent() - self.discount_amount()


class Purchase(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='purchases',
        default=1
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer.name}: {self.product.name}'
