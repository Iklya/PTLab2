from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path(
        'customer/add/',
        views.CustomerCreate.as_view(),
        name='customer_add'
    ),
    path(
        'buy/',
        views.PurchaseCreate.as_view(),
        name='buy'
    ),
]