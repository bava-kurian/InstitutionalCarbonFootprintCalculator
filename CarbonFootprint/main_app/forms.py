from django import forms
from .models import EnergyConsumption, Transportation, WaterUsage, WasteManagement

class EnergyConsumptionForm(forms.ModelForm):
    class Meta:
        model = EnergyConsumption
        exclude = ['yearly_data']

class TransportationForm(forms.ModelForm):
    class Meta:
        model = Transportation
        exclude = ['yearly_data']

class WaterUsageForm(forms.ModelForm):
    class Meta:
        model = WaterUsage
        exclude = ['yearly_data']

class WasteManagementForm(forms.ModelForm):
    class Meta:
        model = WasteManagement
        exclude = ['yearly_data']