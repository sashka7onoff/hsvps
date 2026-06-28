import datetime
from django.db import models
from django.contrib.auth.models import User


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    class Meta:
        ordering = ['-created_at']

    def get_streak(self):
        streak = 0
        today = datetime.date.today()
        check_date = today
        while Entry.objects.filter(habit=self, date=check_date, status='done').exists():
            streak += 1
            check_date -= datetime.timedelta(days=1)
        if streak == 0 and Entry.objects.filter(habit=self, date=today).exists():
            streak = 1
        return streak

    def get_completion_rate(self, days=30):
        start_date = datetime.date.today() - datetime.timedelta(days=days)
        total = Entry.objects.filter(habit=self, date__gte=start_date).count()
        if total == 0:
            return 0
        done = Entry.objects.filter(habit=self, date__gte=start_date, status='done').count()
        return round(done / total * 100)


class Entry(models.Model):
    STATUS_CHOICES = [
        ('empty', 'Нет отметки'),
        ('done', 'Выполнено'),
        ('not_done', 'Не выполнено'),
    ]

    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='entries')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='empty')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['habit', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.habit.name} - {self.date}: {self.get_status_display()}"
