from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm, UserLoginForm, InstitutionForm

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        institution_form = InstitutionForm(request.POST)
        if user_form.is_valid() and institution_form.is_valid():
            user = user_form.save()
            institution = institution_form.save(commit=False)
            institution.user = user
            institution.email = user.email
            institution.password = user.password  # Password will be hashed by User model
            institution.save()
            login(request, user)
            return redirect('home')
    else:
        user_form = UserRegisterForm()
        institution_form = InstitutionForm()
    return render(request, 'users/register.html', {'user_form': user_form, 'institution_form': institution_form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')