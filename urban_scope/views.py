from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .utils import CustomAuthenticationForm, CustomUserCreationForm

def home_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())

            return redirect('states:list')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'home.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)

        if form.is_valid():
            login(request, form.save())

            return redirect('states:list')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

def logout_view(request):
    if request.method == "POST": 
        logout(request) 
        
        return redirect("home")