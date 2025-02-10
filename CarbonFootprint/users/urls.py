from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.auth_view, name='auth'),
    path('institution_form/', views.institution_form_view, name='institution_form'),
    path('logout/', views.user_logout, name='logout'),
]