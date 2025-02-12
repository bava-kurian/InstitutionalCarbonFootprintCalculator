from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Institution

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['name', 'institution_type', 'address', 'city', 'country', 'contact_number']

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))