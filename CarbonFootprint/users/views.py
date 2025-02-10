from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm, UserLoginForm, InstitutionForm

def auth_view(request):
    if request.method == 'POST':
        if 'signup' in request.POST:
            user_form = UserRegisterForm(request.POST)
            login_form = UserLoginForm()  # Empty form for login
            if user_form.is_valid():
                user = user_form.save()
                login(request, user)
                return redirect('institution_form')
        elif 'login' in request.POST:
            login_form = UserLoginForm(request.POST)
            user_form = UserRegisterForm()  # Empty form for signup
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    print("User logged in")
                    return redirect('home')
                else:
                    login_form.add_error(None, "Invalid username or password")
    else:
        user_form = UserRegisterForm()
        login_form = UserLoginForm()
    
    return render(request, 'users/auth.html', {
        'user_form': user_form,
        'login_form': login_form,
    })

def institution_form_view(request):
    if request.method == 'POST':
        institution_form = InstitutionForm(request.POST)
        if institution_form.is_valid():
            institution = institution_form.save(commit=False)
            institution.user = request.user
            institution.email = request.user.email
            institution.password = request.user.password  # Password will be hashed by User model
            institution.save()
            return redirect('home')
    else:
        institution_form = InstitutionForm()
    
    return render(request, 'users/institution_form.html', {
        'institution_form': institution_form,
    })

def user_logout(request):
    logout(request)
    return redirect('auth')