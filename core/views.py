from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, PublishRequestForm, LoginForm
from .models import PublishRequest


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kayıt başarılı.')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('dashboard')
        messages.error(request, 'Geçersiz giriş')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    qs = PublishRequest.objects.filter(facility=request.user.facility)
    return render(request, 'dashboard.html', {'requests': qs})

@login_required
def request_create(request):
    if request.method == 'POST':
        form = PublishRequestForm(request.POST)
        if form.is_valid():
            pr = form.save(commit=False)
            pr.created_by = request.user
            pr.facility = request.user.facility
            pr.full_clean()
            pr.save()
            messages.success(request, 'İstek oluşturuldu')
            return redirect('dashboard')
    else:
        form = PublishRequestForm()
    return render(request, 'request_create.html', {'form': form})