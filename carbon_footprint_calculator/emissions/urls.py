from django.urls import path# filepath: /d:/mini proj worl/InstitutionalCarbonFootprintCalculator/carbon_footprint_calculator/emissions/urls.py
from .views import input_data, results, edit_data, download_pdf

urlpatterns = [
    path('input/', input_data, name='input_data'),
    path('results/<int:emi_data_id>/', results, name='results'),
    path('edit/<int:emi_data_id>/', edit_data, name='edit_data'),
    path('download_pdf/<int:emi_data_id>/', download_pdf, name='download_pdf'),
]