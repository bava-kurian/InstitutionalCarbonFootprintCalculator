from django.contrib import admin
from .models import EmissionFactor, CollegeDetails, EnergyConsumption, Transportation, WaterUsage, WasteManagement

@admin.register(EmissionFactor)
class EmissionFactorAdmin(admin.ModelAdmin):
    list_display = ('category', 'factor')
    search_fields = ('category',)
    list_filter = ('category',)

@admin.register(CollegeDetails)
class CollegeDetailsAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'total_campus_area', 'total_builtup_area', 'lawn_garden_area', 'undeveloped_land_area')
    search_fields = ('name', 'city')
    list_filter = ('city',)

@admin.register(EnergyConsumption)
class EnergyConsumptionAdmin(admin.ModelAdmin):
    list_display = ('year', 'electricity_kwh', 'solar_generation_kwh', 'generator_fuel_liters')
    search_fields = ('year',)
    list_filter = ('year',)

@admin.register(Transportation)
class TransportationAdmin(admin.ModelAdmin):
    list_display = ('year', 'total_students_staff', 'distance_by_bus_km', 'distance_by_personal_vehicles_km', 'distance_by_public_transport_km', 'distance_by_ev_km')
    search_fields = ('year',)
    list_filter = ('year',)

@admin.register(WaterUsage)
class WaterUsageAdmin(admin.ModelAdmin):
    list_display = ('year', 'water_consumed_kl', 'rainwater_harvesting_capacity', 'wastewater_treated_kl')
    search_fields = ('year',)
    list_filter = ('year',)

@admin.register(WasteManagement)
class WasteManagementAdmin(admin.ModelAdmin):
    list_display = ('year', 'waste_generated_tonnes', 'waste_treated_tonnes', 'waste_to_landfill_tonnes')
    search_fields = ('year',)
    list_filter = ('year',)