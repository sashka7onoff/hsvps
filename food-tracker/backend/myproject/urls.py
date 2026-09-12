from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/auth/', include('rest_framework.urls')),
    # Food Tracker — path-based как требовалось: my-domen.ru/food-tracker + /api/food-tracker/
    path('food-tracker/', include('food_tracker.urls')),
    path('api/food-tracker/', include('food_tracker.api_urls')),
    path('', RedirectView.as_view(url='/food-tracker/', permanent=False)),
]
