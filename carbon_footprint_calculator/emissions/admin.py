from django.contrib import admin
from .models import EmissionFactor, EmissionData, EnergyConsumption, FuelConsumption, Transportation, WaterUsage, WasteManagement, PaperUsage

admin.site.register(EmissionFactor)
admin.site.register(EmissionData)
admin.site.register(EnergyConsumption)
admin.site.register(FuelConsumption)
admin.site.register(Transportation)
admin.site.register(WaterUsage)
admin.site.register(WasteManagement)
admin.site.register(PaperUsage)