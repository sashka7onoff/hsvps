from django.contrib import admin
from .models import Task, Plan, TaskPlan


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'priority', 'parent', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    ordering = ['priority', '-created_at']


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'type', 'is_active', 'start_date', 'end_date', 'created_at')
    list_filter = ('type', 'is_active', 'created_at')
    search_fields = ('name', 'user__username')
    ordering = ['-created_at']


@admin.register(TaskPlan)
class TaskPlanAdmin(admin.ModelAdmin):
    list_display = ('task', 'plan', 'is_active', 'added_at')
    list_filter = ('is_active', 'added_at')
    search_fields = ('task__title', 'plan__name')
