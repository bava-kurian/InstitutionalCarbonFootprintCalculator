from django.contrib import admin
from django.urls import path, include
from user.views import home
from emissions import views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include('user.urls')),
    path('emissions/', include('emissions.urls')),
    path('check_year/', views.check_year, name='check_year'),
]
if settings.ADMIN_ENABLED is True:
    urlpatterns += [path('admin/', admin.site.urls),]