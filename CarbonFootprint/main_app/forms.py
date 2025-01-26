from django import forms
from .models import EnergyConsumption, Transportation, WaterUsage, WasteManagement

class EnergyConsumptionForm(forms.ModelForm):
    class Meta:
        model = EnergyConsumption
        fields = '__all__'

class TransportationForm(forms.ModelForm):
    class Meta:
        model = Transportation
        fields = '__all__'

class WaterUsageForm(forms.ModelForm):
    class Meta:
        model = WaterUsage
        fields = '__all__'

class WasteManagementForm(forms.ModelForm):
    class Meta:
        model = WasteManagement
        fields = '__all__'