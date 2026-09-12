from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView

from .models import Customer, Product, Purchase


def index(request):
    products = Product.objects.all()
    customers = Customer.objects.all()

    return render(
        request,
        'shop/index.html',
        {
            'products': products,
            'customers': customers
        }
    )


class CustomerCreate(CreateView):
    model = Customer
    fields = ['name', 'address']

    def get_success_url(self):
        return '/'


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['customer', 'product']

    def form_valid(self, form):
        self.object = form.save()

        customer = self.object.customer

        return HttpResponse(
            f'''
            <h3>Спасибо за покупку, {customer.name}!</h3>
            <p>Общая сумма покупок:
            {customer.total_spent()} руб.</p>
            <p>Накопительная скидка:
            {customer.discount_percent()}%</p>
            <p>Сумма скидки:
            {customer.discount_amount()} руб.</p>
            <p><strong>К оплате:
            {customer.total_with_discount()} руб.</strong></p>
            <p><a href="/">Вернуться в магазин</a></p>
            '''
        )
