from django.urls import path

from .views import (
    CartPageView, add_to_cart,
    remove_from_cart, CheckoutView,
    PaymentView, payment_complete
)

app_name = 'payment'
urlpatterns = [
    path('cart/', CartPageView.as_view(), name='cart'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('payment-complete/', payment_complete, name='payment_complete'),
]