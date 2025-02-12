from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import dashboard, register, institution_register, login, edit_institution

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('institution_register/', institution_register, name='institution_register'),
    path('login/', login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('edit_institution/', edit_institution, name='edit_institution'),
]