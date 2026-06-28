from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from .models import Task, Plan, TaskPlan
from .forms import TaskForm, PlanForm


@login_required
def task_list(request):
    plan_id = request.GET.get('plan')
    status_filter = request.GET.get('status')

    plans = Plan.objects.filter(user=request.user, is_active=True)

    current_plan_obj = None
    if plan_id:
        current_plan_obj = Plan.objects.filter(pk=plan_id, user=request.user).first()

    tasks = Task.objects.filter(user=request.user).select_related('user')

    if current_plan_obj:
        tasks = tasks.filter(plans=current_plan_obj)
    else:
        tasks = tasks.filter(parent__isnull=True)

    if status_filter:
        tasks = tasks.filter(status=status_filter)

    tasks = tasks.prefetch_related('subtasks', 'plans')

    return render(request, 'tasks/tasks_list.html', {
        'tasks': tasks,
        'plans': plans,
        'current_plan': int(plan_id) if plan_id else None,
        'current_plan_obj': current_plan_obj,
        'current_status': status_filter,
    })


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            form.save_m2m()
            return redirect('task_list')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Новая задача'})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task, user=request.user)
    return render(request, 'tasks/task_form.html', {'form': form, 'task': task, 'title': 'Редактировать задачу'})


@login_required
@require_POST
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    return JsonResponse({'success': True})


@login_required
@require_POST
def change_status(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    try:
        data = json.loads(request.body)
        new_status = data.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
            return JsonResponse({'success': True, 'status': task.status})
        return JsonResponse({'error': 'Invalid status'}, status=400)
    except (json.JSONDecodeError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def plan_create(request):
    if request.method == 'POST':
        form = PlanForm(request.POST, user=request.user)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()
            form.save_m2m()
            return redirect('task_list')
    else:
        form = PlanForm(user=request.user)
    return render(request, 'tasks/plan_form.html', {'form': form, 'title': 'Новый план'})


@login_required
def plan_edit(request, pk):
    plan = get_object_or_404(Plan, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PlanForm(request.POST, instance=plan, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = PlanForm(instance=plan, user=request.user)
    return render(request, 'tasks/plan_form.html', {'form': form, 'plan': plan, 'title': 'Редактировать план'})


@login_required
@require_POST
def plan_delete(request, pk):
    plan = get_object_or_404(Plan, pk=pk, user=request.user)
    plan.delete()
    return JsonResponse({'success': True})


@login_required
def task_search(request):
    q = request.GET.get('q', '')
    plan_id = request.GET.get('plan_id')
    tasks = Task.objects.filter(user=request.user, title__icontains=q).exclude(plans__id=plan_id)[:20]
    return JsonResponse([{'id': t.id, 'title': t.title} for t in tasks], safe=False)


@login_required
@require_POST
def add_task_to_plan(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id, user=request.user)
    try:
        data = json.loads(request.body)
        task_id = data.get('task_id')
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        TaskPlan.objects.get_or_create(task=task, plan=plan)
        return JsonResponse({'success': True})
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid data'}, status=400)


@login_required
@require_POST
def remove_task_from_plan(request, plan_id, task_id):
    plan = get_object_or_404(Plan, pk=plan_id, user=request.user)
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    TaskPlan.objects.filter(task=task, plan=plan).delete()
    return JsonResponse({'success': True})
