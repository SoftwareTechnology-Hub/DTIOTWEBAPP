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
            username=email,          # IMPORTANT (internal)
            email=email,
            first_name=name,          # Name stored here
            phone=phone
        )
        user.set_password(password)
        user.save()

        messages.success(request, 'Signup successful. Please login.')
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

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'users/login.html')
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import secrets
@login_required
def profile(request):
    user = request.user  # get the logged-in user
    return render(request, 'users/profile.html', {'user': user})

@login_required
@login_required
def regenerate_api_key(request):
    if request.method == "POST":
        user = request.user
        user.api_key = secrets.token_hex(32)  # generate new secure API key
        user.save()
        messages.success(request, "New API Key generated successfully!")
    return redirect('/auth/profile')

from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    """
    Logs out the user and clears the session completely.
    """
    logout(request)  # Django clears the session and cookies automatically
    return redirect('login')  # Redirect to your login page
def notifications(request):
    # Placeholder for notifications view
    return render(request, 'users/notifications.html')