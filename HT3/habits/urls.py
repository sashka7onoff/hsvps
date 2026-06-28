from django.urls import path
from . import views

urlpatterns = [
    path('', views.habit_list, name='habit_list'),
    path('create/', views.habit_create, name='habit_create'),
    path('<int:pk>/', views.habit_detail, name='habit_detail'),
    path('<int:pk>/edit/', views.habit_edit, name='habit_edit'),
    path('mark/', views.mark_entry, name='mark_entry'),
    path('<int:pk>/toggle/', views.toggle_habit_active, name='toggle_habit_active'),
    path('<int:pk>/delete/', views.delete_habit, name='delete_habit'),
]
