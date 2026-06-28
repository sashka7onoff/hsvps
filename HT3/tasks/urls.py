from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('<int:pk>/status/', views.change_status, name='change_status'),
    path('search/', views.task_search, name='task_search'),
    path('plans/create/', views.plan_create, name='plan_create'),
    path('plans/<int:pk>/edit/', views.plan_edit, name='plan_edit'),
    path('plans/<int:pk>/delete/', views.plan_delete, name='plan_delete'),
    path('plans/<int:plan_id>/add-task/', views.add_task_to_plan, name='add_task_to_plan'),
    path('plans/<int:plan_id>/remove-task/<int:task_id>/', views.remove_task_from_plan, name='remove_task_from_plan'),
]
