from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Digite seu usuário'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Digite sua senha'
        })

def home_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            print('OK')
            return redirect('states:list')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'home.html', {'form': form})

def logout_view(request):
    if request.method == "POST": 
        logout(request) 
        return redirect("home")