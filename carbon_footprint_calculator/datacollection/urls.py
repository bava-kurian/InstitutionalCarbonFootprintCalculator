from django.urls import path
from .views import collect_data, data_collection_success

urlpatterns = [
    path('collect/', collect_data, name='collect_data'),
    path('success/', data_collection_success, name='data_collection_success'),
]
