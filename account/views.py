from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse_lazy

from .forms import (
    SignInForm,
    PasswordChangeForm,
)

from .models import Account

def login_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f'you are already sign in as {user.username}!')

    if request.POST:
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(email = request.POST['email'], password=request.POST['password'])
            if user:
                login(request, user)
                return redirect('profile:home')
    else:
        form = SignInForm()
    context = {'form': form, 'user': user}
    return render(request, 'registration/login.html', context=context)

def password_change_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'You can\'t access this page!')
    if request.POST:
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = authenticate(email = user.email, password = request.POST['password1'])
            if user:
                user.set_password(request.POST['password2'])
                user.save()
                logout(request)
                return redirect('profile:password_change_done')
    else:
        form = PasswordChangeForm(user)
    context = {'form': form, 'user': user}
    return render(request, 'registration/password_change_form.html', context=context)

def profile_view(request, username, *args, **kwargs):
    user = request.user
    try:
        profile = Account.objects.get(username = username)
    except Account.DoesNotExist:
        raise ValueError('can\'t reach this profile')
    context = {'profile': profile, 'user': user}
    return render(request, 'profile/profile_detail.html', context=context)
