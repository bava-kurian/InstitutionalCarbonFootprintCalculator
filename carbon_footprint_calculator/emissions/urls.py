from django.urls import path# filepath: /d:/mini proj worl/InstitutionalCarbonFootprintCalculator/carbon_footprint_calculator/emissions/urls.py
from .views import input_data, results, edit_data, download_pdf, monthly_data_entry, monthly_data_summary

urlpatterns = [
    path('input/', input_data, name='input_data'),
    path('results/<int:emi_data_id>/', results, name='results'),
    path('edit/<int:emi_data_id>/', edit_data, name='edit_data'),
    path('download_pdf/<int:emi_data_id>/', download_pdf, name='download_pdf'),
    path('monthly-data/', monthly_data_entry, name='monthly_data_entry'),
    path('monthly-summary/', monthly_data_summary, name='monthly_data_summary'),
]