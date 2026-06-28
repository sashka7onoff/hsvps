from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart_view, name='cart'),
    path('blanks/', views.blanks_view, name='blanks'),
    path('blanks/<int:blank_id>/configure/', views.configure_view, name='configure'),
    path('profile/', views.profile_view, name='profile'),
    path('balance/', views.balance_view, name='balance'),
    path('oferta/', views.oferta_view, name='oferta'),
    path('check-login/', views.check_login, name='check_login'),
    path('check-email/', views.check_email, name='check_email'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('delete-blank/<int:blank_id>/', views.delete_blank, name='delete_blank'),
    path('recount-product/', views.recount_product, name='recount_product'),
    path('update-blank-index/', views.update_blank_index, name='update_blank_index'),
    path('manage-cart/', views.manage_cart, name='manage_cart'),
    path('upload-blank/', views.upload_blank, name='upload_blank'),
    path('download-filled/', views.download_filled, name='download_filled'),
]
