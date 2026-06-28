import calendar
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Prefetch
from .models import Habit, Entry
from .forms import HabitForm


@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user).select_related('user')

    today = datetime.date.today()
    last_5_days = [today - datetime.timedelta(days=i) for i in range(5)]

    entries_map = {}
    for entry in Entry.objects.filter(
        habit__in=habits,
        date__in=last_5_days
    ).select_related('habit'):
        entries_map.setdefault(entry.habit_id, {})[entry.date.isoformat()] = entry.status

    habit_data = []
    for habit in habits:
        streak = habit.get_streak()
        completion = habit.get_completion_rate()
        entries = {}
        for d in last_5_days:
            entries[d.isoformat()] = entries_map.get(habit.id, {}).get(d.isoformat(), 'empty')
        habit_data.append({
            'habit': habit,
            'entries': entries,
            'streak': streak,
            'completion': completion,
        })

    form = HabitForm()
    return render(request, 'habits/habit_list.html', {
        'habit_data': habit_data,
        'form': form,
        'today': today,
    })


@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('habit_list')
    else:
        form = HabitForm()
    return render(request, 'habits/habit_form.html', {'form': form, 'title': 'Новая привычка'})


@login_required
def habit_edit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('habit_list')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'habits/habit_form.html', {'form': form, 'habit': habit, 'title': 'Редактировать привычку'})


@login_required
@require_POST
def mark_entry(request):
    habit = get_object_or_404(Habit, pk=request.POST.get('habit_id'), user=request.user)
    date_str = request.POST.get('date')
    status = request.POST.get('status')
    date_obj = datetime.date.fromisoformat(date_str)

    entry, created = Entry.objects.update_or_create(
        habit=habit,
        date=date_obj,
        defaults={'status': status},
    )

    streak = habit.get_streak()
    return JsonResponse({
        'status': entry.status,
        'streak': streak,
    })


@login_required
@require_POST
def toggle_habit_active(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    habit.is_active = not habit.is_active
    habit.save()
    return JsonResponse({'is_active': habit.is_active})


@login_required
@require_POST
def delete_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    habit.delete()
    return JsonResponse({'success': True})


@login_required
def habit_detail(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)

    year = request.GET.get('year')
    month = request.GET.get('month')

    if year and month:
        year = int(year)
        month = int(month)
    else:
        today = datetime.date.today()
        year = today.year
        month = today.month

    today = datetime.date.today()

    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, month)
    month_name_ru = [
        '', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
        'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
    ][month]
    year_str = str(year)

    first_day = datetime.date(year, month, 1)
    last_day = datetime.date(year, month, calendar.monthrange(year, month)[1])

    entries = {
        e.date: e
        for e in Entry.objects.filter(habit=habit, date__gte=first_day, date__lte=last_day)
    }

    calendar_weeks = []
    for week in month_days:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append(None)
            else:
                date_obj = datetime.date(year, month, day)
                entry = entries.get(date_obj)
                week_data.append({
                    'day': day,
                    'date_str': date_obj.isoformat(),
                    'is_today': date_obj == today,
                    'status': entry.status if entry else 'empty',
                })
        calendar_weeks.append(week_data)

    month_entries = Entry.objects.filter(habit=habit, date__gte=first_day, date__lte=last_day)
    done_count = month_entries.filter(status='done').count()
    not_done_count = month_entries.filter(status='not_done').count()
    empty_count = month_entries.filter(status='empty').count()
    total_marked = done_count + not_done_count
    completion_rate = round(done_count / total_marked * 100) if total_marked > 0 else 0

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    return render(request, 'habits/habit_detail.html', {
        'habit': habit,
        'calendar_weeks': calendar_weeks,
        'month_name': month_name_ru,
        'year_str': year_str,
        'today': today,
        'year': year,
        'month': month,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'done_count': done_count,
        'not_done_count': not_done_count,
        'empty_count': empty_count,
        'completion_rate': completion_rate,
    })
