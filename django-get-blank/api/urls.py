from django.urls import path
from . import views

urlpatterns = [
    path('api/add-product/', views.add_product, name='api_add_product'),
    path('api/me/', views.me, name='api_me'),
    path('api/carts/', views.carts_list, name='api_carts'),
    path('api/cart/<int:cart_id>/', views.cart_detail, name='api_cart_detail'),
    path('api/cart/select/', views.cart_select, name='api_cart_select'),
    path('api/cart/create/', views.cart_create, name='api_cart_create'),
    path('api/product/<int:product_id>/', views.delete_product, name='api_delete_product'),
]
