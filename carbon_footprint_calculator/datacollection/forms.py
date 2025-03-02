from django import forms
from .models import MonthlyData

class ElectricityForm(forms.ModelForm):
    class Meta:
        model = MonthlyData
        fields = ['user', 'year', 'month', 'electricity_kwh']

class SolarGenerationForm(forms.ModelForm):
    class Meta:
        model = MonthlyData
        fields = ['user', 'year', 'month', 'solar_generation_kwh']

class GeneratorFuelForm(forms.ModelForm):
    class Meta:
        model = MonthlyData
        fields = ['user', 'year', 'month', 'generator_fuel_liters']

class DieselForm(forms.ModelForm):
    class Meta:
        model = MonthlyData
        fields = ['user', 'year', 'month', 'diesel_liters']

class PetrolForm(forms.ModelForm):
    class Meta:
        model = MonthlyData
        fields = ['user', 'year', 'month', 'petrol_liters']

class LPGForm(forms.ModelForm):
    class Meta:
        model = MonthlyData
        fields = ['user', 'year', 'month', 'lpg_kg']

class BusDistanceForm(forms.ModelForm):
    class Meta:
        model = MonthlyData
        fields = ['user', 'year', 'month', 'distance_by_bus_km']

class PersonalDistanceForm(forms.ModelForm):
    class Meta:
        model = MonthlyData
        fields = ['user', 'year', 'month', 'distance_by_personal_km']

class PublicDistanceForm(forms.ModelForm):
    class Meta:
        model = MonthlyData
        fields = ['user', 'year', 'month', 'distance_by_public_km']

class EVDistanceForm(forms.ModelForm):
    class Meta:
        model = MonthlyData
        fields = ['user', 'year', 'month', 'distance_by_ev_km']

class WaterConsumedForm(forms.ModelForm):
    class Meta:
        model = MonthlyData
        fields = ['user', 'year', 'month', 'water_consumed_kl']

class WastewaterTreatedForm(forms.ModelForm):
    class Meta:
        model = MonthlyData
        fields = ['user', 'year', 'month', 'wastewater_treated_kl']

class OrganicWasteForm(forms.ModelForm):
    class Meta:
        model = MonthlyData
        fields = ['user', 'year', 'month', 'organic_waste_kg']

class PlasticWasteForm(forms.ModelForm):
    class Meta:
        model = MonthlyData
        fields = ['user', 'year', 'month', 'plastic_waste_kg']

class SewageForm(forms.ModelForm):
    class Meta:
        model = MonthlyData
        fields = ['user', 'year', 'month', 'sewage_liters']

class EWasteForm(forms.ModelForm):
    class Meta:
        model = MonthlyData
        fields = ['user', 'year', 'month', 'ewaste_kg']

class PaperForm(forms.ModelForm):
    class Meta:
        model = MonthlyData
        fields = ['user', 'year', 'month', 'paper_kg']
