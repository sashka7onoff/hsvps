from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from habits.models import Habit, Entry
from tasks.models import Task, Plan
import datetime


@login_required
def home(request):
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)

    habits = Habit.objects.filter(user=request.user, is_active=True)
    total_habits = habits.count()

    entries_this_week = Entry.objects.filter(
        habit__user=request.user,
        date__gte=week_ago,
        status='done'
    ).count()

    tasks_todo = Task.objects.filter(user=request.user, status='todo').count()
    tasks_in_progress = Task.objects.filter(user=request.user, status='in_progress').count()
    tasks_done = Task.objects.filter(user=request.user, status='done').count()

    active_plans = Plan.objects.filter(
        task__user=request.user,
        is_active=True
    ).distinct().count()

    streaks = []
    for habit in habits[:5]:
        streak = 0
        check_date = today
        while Entry.objects.filter(habit=habit, date=check_date, status='done').exists():
            streak += 1
            check_date -= datetime.timedelta(days=1)
        streaks.append({'habit': habit, 'streak': streak})

    context = {
        'total_habits': total_habits,
        'entries_this_week': entries_this_week,
        'tasks_todo': tasks_todo,
        'tasks_in_progress': tasks_in_progress,
        'tasks_done': tasks_done,
        'active_plans': active_plans,
        'streaks': streaks,
    }
    return render(request, 'home.html', context)
