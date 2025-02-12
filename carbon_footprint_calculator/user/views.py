from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Institution, User
from .forms import InstitutionForm, UserRegistrationForm, LoginForm

def home(request):
    return render(request, 'user/home.html')

@login_required
def dashboard(request):
    user = request.user
    emissions = user.emissiondata_set.all()
    institution = Institution.objects.get(user=user)
    return render(request, 'user/dashboard.html', {
        'emissions': emissions,
        'institution': institution
    })

def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            auth_login(request, user)
            return redirect('institution_register')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'user/register.html', {'user_form': user_form})

@login_required
def institution_register(request):
    if request.method == "POST":
        institution_form = InstitutionForm(request.POST)
        if institution_form.is_valid():
            institution = institution_form.save(commit=False)
            institution.user = request.user
            institution.save()
            return redirect('dashboard')
    else:
        institution_form = InstitutionForm()
    return render(request, 'user/institution_register.html', {'institution_form': institution_form})

@login_required
def edit_institution(request):
    institution = Institution.objects.get(user=request.user)
    if request.method == "POST":
        institution_form = InstitutionForm(request.POST, instance=institution)
        if institution_form.is_valid():
            institution_form.save()
            return redirect('dashboard')
    else:
        institution_form = InstitutionForm(instance=institution)
    return render(request, 'user/edit_institution.html', {'institution_form': institution_form})

def login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})