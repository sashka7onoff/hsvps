from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        ('Личные данные', {'fields': ('name', 'last_name', 'email', 'gender', 'b_day', 'b_month', 'b_year')}),
        ('Баланс и тариф', {'fields': ('balance', 'tariff')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('login', 'email', 'name', 'balance', 'is_staff')
    search_fields = ('login', 'email', 'name')
    ordering = ('login',)


admin.site.register(User, UserAdmin)
