from django.urls import path, re_path
from django.views.generic import TemplateView

# SPA fallback: nginx отдаёт статику, но при прямом proxy на Django нужен fallback
urlpatterns = [
    path('', TemplateView.as_view(template_name='food_tracker/app.html'), name='food-tracker-app'),
    re_path(r'^.*$', TemplateView.as_view(template_name='food_tracker/app.html')),
]
