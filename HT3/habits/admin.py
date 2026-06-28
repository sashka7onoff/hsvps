from django.contrib import admin
from .models import Habit, Entry


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'user__username')
    ordering = ['-created_at']


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('habit', 'date', 'status', 'created_at')
    list_filter = ('status', 'date')
    search_fields = ('habit__name', 'notes')
    ordering = ['-date']
