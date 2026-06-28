from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('payment/create/', views.create_payment, name='create'),
    path('payment/webhook/', views.payment_webhook, name='webhook'),
    path('payment/success/', views.payment_success, name='success'),
]
