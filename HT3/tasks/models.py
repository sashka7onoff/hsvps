from django.db import models
from django.contrib.auth.models import User


class Plan(models.Model):
    TYPE_CHOICES = [
        ("year", "Год"),
        ("month", "Месяц"),
        ("week", "Неделя"),
        ("day", "День"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plans')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    class Meta:
        ordering = ['-created_at']


class Task(models.Model):
    STATUS_CHOICES = [
        ("todo", "К выполнению"),
        ("in_progress", "В процессе"),
        ("done", "Выполнено"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="subtasks",
        on_delete=models.CASCADE,
    )
    plans = models.ManyToManyField(Plan, through="TaskPlan")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    priority = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['priority', '-created_at']


class TaskPlan(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_plans")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="task_plans")
    added_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['task', 'plan']

    def __str__(self):
        return f"{self.task} -> {self.plan}"
