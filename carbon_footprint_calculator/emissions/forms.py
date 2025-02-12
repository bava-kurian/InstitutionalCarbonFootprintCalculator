from django import forms
from .models import EmissionData, EnergyConsumption, FuelConsumption, Transportation, WaterUsage, WasteManagement

class EmissionDataForm(forms.ModelForm):
    class Meta:
        model = EmissionData
        fields = ['year']

class EnergyConsumptionForm(forms.ModelForm):
    class Meta:
        model = EnergyConsumption
        fields = ['electricity_kwh', 'solar_generation_kwh', 'generator_fuel_liters']

class FuelConsumptionForm(forms.ModelForm):
    class Meta:
        model = FuelConsumption
        fields = ['diesel_liters', 'petrol_liters', 'lpg_kg']

class TransportationForm(forms.ModelForm):
    class Meta:
        model = Transportation
        fields = ['distance_by_bus_km', 'distance_by_personal_km', 'distance_by_public_km', 'distance_by_ev_km']

class WaterUsageForm(forms.ModelForm):
    class Meta:
        model = WaterUsage
        fields = ['water_consumed_kl', 'wastewater_treated_kl']

class WasteManagementForm(forms.ModelForm):
    class Meta:
        model = WasteManagement
        fields = ['organic_waste_kg', 'plastic_waste_kg', 'sewage_liters']