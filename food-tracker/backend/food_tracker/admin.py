from django.contrib import admin
from .models import MealEntry

@admin.register(MealEntry)
class MealEntryAdmin(admin.ModelAdmin):
    list_display = ('user','eaten_at','meal_type','is_planned','portion','rating')
    list_filter = ('meal_type','is_planned','portion','rating')
    search_fields = ('note',)
