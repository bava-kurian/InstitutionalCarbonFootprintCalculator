from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('input', views.input_data, name='input_data'),
    path('results/', views.results_view, name='results_view'),
    path('calculate/', views.calculate_emissions_view, name='calculate_emissions'),
]