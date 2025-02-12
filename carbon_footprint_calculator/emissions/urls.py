from django.urls import path
from .views import input_data, results, edit_data

urlpatterns = [
    path('input/', input_data, name='input_data'),
    path('results/<int:emi_data_id>/', results, name='results'),
    path('edit/<int:emi_data_id>/', edit_data, name='edit_data'),
]