from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Count
import json
from .models import Category, Subcategory, Note
from .forms import CategoryForm, SubcategoryForm, NoteForm


@login_required
def note_list(request):
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')
    search = request.GET.get('q')

    notes = Note.objects.filter(user=request.user).select_related('category', 'subcategory')

    if category_id:
        notes = notes.filter(category_id=category_id)
    if subcategory_id:
        notes = notes.filter(subcategory_id=subcategory_id)
    if search:
        notes = notes.filter(title__icontains=search) | notes.filter(description__icontains=search)

    categories = Category.objects.filter(user=request.user).annotate(note_count=Count('notes'))

    current_category = None
    current_subcategory = None
    subcategories = []
    if category_id:
        current_category = Category.objects.filter(pk=category_id, user=request.user).first()
        if current_category:
            subcategories = Subcategory.objects.filter(category=current_category).annotate(note_count=Count('notes'))
    else:
        subcategories = []

    if subcategory_id:
        current_subcategory = Subcategory.objects.filter(pk=subcategory_id, user=request.user).first()

    return render(request, 'notes/note_list.html', {
        'notes': notes,
        'categories': categories,
        'current_category': current_category,
        'current_subcategory': current_subcategory,
        'subcategories': subcategories,
        'search': search,
    })


@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('note_list')
    else:
        cat_id = request.GET.get('category')
        sub_id = request.GET.get('subcategory')
        form = NoteForm(user=request.user)
        if cat_id:
            form.fields['category'].initial = int(cat_id)
        if sub_id:
            form.fields['subcategory'].initial = int(sub_id)
    return render(request, 'notes/note_form.html', {'form': form, 'title': 'Новая заметка'})


@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note, user=request.user)
    return render(request, 'notes/note_form.html', {'form': form, 'note': note, 'title': 'Редактировать'})


@login_required
@require_POST
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.delete()
    return JsonResponse({'success': True})


@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'notes/note_detail.html', {'note': note})


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.user = request.user
            cat.save()
            return redirect('note_list')
    else:
        form = CategoryForm()
    return render(request, 'notes/category_form.html', {'form': form, 'title': 'Новая категория'})


@login_required
def subcategory_create(request):
    if request.method == 'POST':
        form = SubcategoryForm(request.POST, user=request.user)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.user = request.user
            sub.save()
            return redirect('note_list')
    else:
        form = SubcategoryForm(user=request.user)
    return render(request, 'notes/subcategory_form.html', {'form': form, 'title': 'Новая подкатегория'})


@login_required
@require_POST
def category_delete(request, pk):
    cat = get_object_or_404(Category, pk=pk, user=request.user)
    cat.delete()
    return JsonResponse({'success': True})


@login_required
@require_POST
def subcategory_delete(request, pk):
    sub = get_object_or_404(Subcategory, pk=pk, user=request.user)
    sub.delete()
    return JsonResponse({'success': True})


@login_required
def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subs = Subcategory.objects.filter(category_id=category_id, user=request.user)
    return JsonResponse([{'id': s.id, 'name': s.name} for s in subs], safe=False)
