from django.contrib import admin
from .models import Institution

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'type', 'city', 'country', 'date_registered')
    search_fields = ('name', 'email', 'city', 'country')
    list_filter = ('type', 'city', 'country')