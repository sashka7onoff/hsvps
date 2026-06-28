from django.contrib import admin
from .models import Cart, Product, Blank


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'ts_created', 'deleted')
    list_filter = ('deleted',)
    search_fields = ('name', 'user__login')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cart', 'color', 'size', 'amount', 'price', 'deleted')
    list_filter = ('deleted',)
    search_fields = ('link',)


@admin.register(Blank)
class BlankAdmin(admin.ModelAdmin):
    list_display = ('blank_id', 'user', 'blank_filename_original', 'ts_created')
    search_fields = ('blank_filename_original', 'user__login')
