from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .serializers import TaskViewSet, PlanViewSet, TaskPlanViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='api-tasks')
router.register(r'plans', PlanViewSet, basename='api-plans')
router.register(r'task-plans', TaskPlanViewSet, basename='api-task-plans')

urlpatterns = [
    path('', include(router.urls)),
]
