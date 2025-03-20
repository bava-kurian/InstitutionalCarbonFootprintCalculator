from django.contrib import admin
from .models import (
    EmissionFactor, EmissionData, EnergyConsumption, 
    FuelConsumption, Transportation, WaterUsage, 
    WasteManagement, PaperUsage, MonthlyEmissionData,
    FoodConsumption, Refrigerants
)

class EmissionDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'year', 'total_emissions')

class EnergyConsumptionAdmin(admin.ModelAdmin):
    list_display = ('emi_data', 'electricity_kwh', 'solar_generation_kwh', 'generator_fuel_liters')

class FuelConsumptionAdmin(admin.ModelAdmin):
    list_display = ('emi_data', 'diesel_liters', 'petrol_liters', 'lpg_kg')

class TransportationAdmin(admin.ModelAdmin):
    list_display = ('emi_data', 'distance_by_bus_km', 'distance_by_personal_km', 'distance_by_public_km', 'distance_by_ev_km')

class WaterUsageAdmin(admin.ModelAdmin):
    list_display = ('emi_data', 'water_consumed_kl', 'wastewater_treated_kl')

class WasteManagementAdmin(admin.ModelAdmin):
    list_display = ('emi_data', 'organic_waste_kg', 'plastic_waste_kg', 'sewage_liters', 'ewaste_kg')

class PaperUsageAdmin(admin.ModelAdmin):
    list_display = ('emi_data', 'paper_kg')

class MonthlyEmissionDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'year', 'month', 'is_complete', 'electricity_kwh', 
                   'diesel_liters', 'water_consumed_kl', 'paper_kg')
    list_filter = ('user', 'year', 'month', 'is_complete')
    search_fields = ['user__username', 'year', 'month']
    ordering = ['-year', '-month']

class FoodConsumptionAdmin(admin.ModelAdmin):
    list_display = ('emi_data', 'red_meat_kg', 'poultry_kg', 'vegetables_kg')

class RefrigerantsAdmin(admin.ModelAdmin):
    list_display = ('emi_data', 'r134a_kg', 'r410a_kg')

admin.site.register(EmissionFactor)
admin.site.register(EmissionData, EmissionDataAdmin)
admin.site.register(EnergyConsumption, EnergyConsumptionAdmin)
admin.site.register(FuelConsumption, FuelConsumptionAdmin)
admin.site.register(Transportation, TransportationAdmin)
admin.site.register(WaterUsage, WaterUsageAdmin)
admin.site.register(WasteManagement, WasteManagementAdmin)
admin.site.register(PaperUsage, PaperUsageAdmin)
admin.site.register(MonthlyEmissionData, MonthlyEmissionDataAdmin)
admin.site.register(FoodConsumption, FoodConsumptionAdmin)
admin.site.register(Refrigerants, RefrigerantsAdmin)