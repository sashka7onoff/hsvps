from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Q
from rest_framework import viewsets, permissions, views, response
from .models import MealEntry
from .serializers import MealEntrySerializer

class MealEntryViewSet(viewsets.ModelViewSet):
    serializer_class = MealEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = MealEntry.objects.filter(user=self.request.user)
        period = self.request.query_params.get('period')
        if period == 'today':
            qs = qs.filter(eaten_at__date=timezone.now().date())
        elif period == 'week':
            qs = qs.filter(eaten_at__gte=timezone.now() - timedelta(days=7))
        elif period == 'month':
            qs = qs.filter(eaten_at__gte=timezone.now() - timedelta(days=30))
        # доп фильтры
        for f in ['rating','meal_type','portion']:
            v = self.request.query_params.get(f)
            if v: qs = qs.filter(**{f: v})
        return qs

class StatsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        period = request.query_params.get('period', 'week')
        qs = MealEntry.objects.filter(user=request.user)
        if period == 'today':
            qs = qs.filter(eaten_at__date=timezone.now().date())
        elif period == 'week':
            qs = qs.filter(eaten_at__gte=timezone.now() - timedelta(days=7))
        elif period == 'month':
            qs = qs.filter(eaten_at__gte=timezone.now() - timedelta(days=30))

        total = qs.count()
        planned = qs.filter(is_planned=True).count()
        impulsive = qs.filter(is_planned=False).count()
        junk_count = sum(1 for e in qs if e.junk_items)
        ratings = qs.values('rating').annotate(c=Count('id'))
        # топ триггеры
        from collections import Counter
        counter = Counter()
        for e in qs:
            for r in e.reasons: counter[r]+=1
        triggers = counter.most_common(3)
        # стрики: дни без мусора (упрощенно)
        # heatmap по дням
        heatmap = qs.values('eaten_at__date').annotate(c=Count('id'), bad=Count('id', filter=Q(rating='bad')))

        return response.Response({
            'total': total,
            'planned': planned,
            'impulsive': impulsive,
            'junk_count': junk_count,
            'ratings': {r['rating']: r['c'] for r in ratings},
            'triggers': triggers,
            'heatmap': list(heatmap),
        })
