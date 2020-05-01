from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from articles.forms import CommentForm

User = get_user_model()
# Create your views here.
def index(request):
    return render(request, 'accounts/index.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:signup_confirm')
    else:
        form = CustomUserCreationForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/signup.html', context)

def signup_confirm(request):
    return render(request, 'accounts/signup_confirm.html')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('articles:index')

def profile(request, username):
    user = get_object_or_404(User, username=username)
    form = CommentForm()
    context = {
        'user': user,
        'form': form
    }
    return render(request, 'accounts/profile.html', context)

def follow(request, username):
    user = get_object_or_404(User, username=username)
    if user.followers.filter(username=request.user.username).exists():
        user.followers.remove(request.user)
    else:
        user.followers.add(request.user)
    return redirect('accounts:profile', username)
