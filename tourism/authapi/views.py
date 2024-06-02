from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .forms import *
from .models import CustomUser


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(
                request, 'You are successfully registered. Now you can login.')
            return redirect('login')
        else:
            messages.error(request, 'Something went wrong. Please try again.')
    else:
        form = UserRegistrationForm()
    return render(request, 'authapi/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = CustomUser.objects.filter(email=email).first()
            if user and user.check_password(password):
                request.session['user_id'] = user.id
                messages.success(
                    request, 'You have been logged in successfully.')
                if user.is_admin:
                    return redirect('admin_dashboard')
                else:
                    return redirect(reverse('user_profile'))
            else:
                messages.error(request, 'Invalid email or password')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = LoginForm()
    return render(request, 'authapi/signin.html', {'form': form})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
    else:
        messages.error(request, 'You are not logged in.')
    return redirect('login')


