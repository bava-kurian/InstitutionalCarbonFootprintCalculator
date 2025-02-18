from django.urls import path
from .views import input_data, results, edit_data, handle_query
from . import pdf_views

urlpatterns = [
    path('input/', input_data, name='input_data'),
    path('results/<int:emi_data_id>/', results, name='results'),
    path('edit/<int:emi_data_id>/', edit_data, name='edit_data'),
    path('results/<int:emi_data_id>/pdf/', pdf_views.render_pdf_view, name='render_pdf_view'),
    path('handle_query/', handle_query, name='handle_query'),
]