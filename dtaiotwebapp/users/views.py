from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('signup')

        user = CustomUser(
            username=email,      # 🔑 KEY POINT
            email=email,
            first_name=name,
            phone=phone
        )
        user.set_password(password)
        user.save()

        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')

    return render(request, 'users/signup.html')
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'users/login.html')
