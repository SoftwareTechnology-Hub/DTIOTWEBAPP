from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
import re
import html

def signup(request):
    if request.method == 'POST':
        # Get and sanitize inputs
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Validation: Check if fields are empty
        if not all([name, email, phone, password, confirm_password]):
            messages.error(request, 'All fields are required')
            return redirect('signup')

        # Sanitize name - remove any HTML/script tags
        name = html.escape(name)
        # Allow only letters and spaces in name
        if not re.match(r'^[a-zA-Z\s]{2,50}$', name):
            messages.error(request, 'Name must contain only letters and be 2-50 characters')
            return redirect('signup')

        # Validate email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messages.error(request, 'Invalid email format')
            return redirect('signup')

        # Sanitize and validate phone - remove any non-numeric characters except + and -
        phone = re.sub(r'[^\d+\-\s()]', '', phone)
        if len(phone) < 10:
            messages.error(request, 'Phone number must be at least 10 digits')
            return redirect('signup')

        # Check password strength
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters')
            return redirect('signup')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('signup')

        # Create user with sanitized data
        user = CustomUser(
            username=email,
            email=email,
            first_name=name,
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
from django.contrib.auth.decorators import login_required
from .models import Notification
def notifications(request):
    notifications = Notification.objects.filter(is_active=True).order_by("-created_at")
    return render(request, "users/notifications.html", {
        "notifications": notifications
    })
