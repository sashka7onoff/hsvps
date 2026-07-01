from django.urls import path
from . import views

urlpatterns = [
    path('api/add-product/', views.add_product, name='api_add_product'),
    path('api/me/', views.me, name='api_me'),
]
