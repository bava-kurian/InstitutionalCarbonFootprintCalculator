from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('emissions/', include('emissions.urls')),
    path('datacollection/', include('datacollection.urls')),
]
