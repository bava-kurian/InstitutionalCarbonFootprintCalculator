from django.urls import path, include
from user import views as user_views

urlpatterns = [
    path('emissions/', include('emissions.urls')),
]