from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Digite seu usuário'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Digite sua senha'
        })

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Digite seu usuário'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Digite sua senha'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Digite sua senha novamente'
        })