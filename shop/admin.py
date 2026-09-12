from django.contrib import admin

from .models import Customer, Product, Purchase


admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Purchase)