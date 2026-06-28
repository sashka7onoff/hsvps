from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from .models import User


def login_view(request):
    from django.contrib.auth import authenticate
    if request.user.is_authenticated:
        return redirect('cart')
    error = False
    if request.method == 'POST':
        login_input = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, username=login_input, password=password)
        if user is not None:
            login(request, user)
            return redirect('cart')
        else:
            error = True
    return render(request, 'main.html', {'view': 'login', 'login_error': error})


def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('index')


def registration_view(request):
    if request.user.is_authenticated:
        return redirect('cart')
    if request.method == 'POST':
        login_input = request.POST.get('login')
        email = request.POST.get('email')
        password = request.POST.get('password')
        promocode = request.POST.get('promocode', '')

        if User.objects.filter(login=login_input).exists():
            return render(request, 'main.html', {'view': 'registration', 'login_taken': True, 'promocode': promocode})
        if User.objects.filter(email=email).exists():
            return render(request, 'main.html', {'view': 'registration', 'email_taken': True, 'promocode': promocode})

        user = User.objects.create_user(login=login_input, email=email, password=password)
        login(request, user)

        from main.models import Cart
        Cart.objects.create(user=user, name='Список 1')

        return redirect('cart')

    promocode = request.GET.get('promocode', '')
    return render(request, 'main.html', {'view': 'registration', 'promocode': promocode})
