from django.db import models
from user.models import User

class EmissionFactor(models.Model):
    electricity = models.FloatField()
    diesel = models.FloatField()
    petrol = models.FloatField()
    lpg = models.FloatField()
    water_supply = models.FloatField()
    wastewater_treatment = models.FloatField()
    organic_waste = models.FloatField()
    plastic_waste = models.FloatField()
    sewage_treatment = models.FloatField()
    paper = models.FloatField()
    refrigerant_gwp = models.FloatField()

class EmissionData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    total_emissions = models.FloatField(default=0.0)
    electricity_emissions = models.FloatField(default=0.0)
    diesel_emissions = models.FloatField(default=0.0)
    petrol_emissions = models.FloatField(default=0.0)
    lpg_emissions = models.FloatField(default=0.0)
    public_transport_emissions = models.FloatField(default=0.0)
    water_supply_emissions = models.FloatField(default=0.0)
    plastic_waste_emissions = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('user', 'year')

class EnergyConsumption(models.Model):
    emi_data = models.OneToOneField(EmissionData, on_delete=models.CASCADE, primary_key=True)
    electricity_kwh = models.FloatField()
    solar_generation_kwh = models.FloatField()
    generator_fuel_liters = models.FloatField()

class FuelConsumption(models.Model):
    emi_data = models.OneToOneField(EmissionData, on_delete=models.CASCADE, primary_key=True)
    diesel_liters = models.FloatField()
    petrol_liters = models.FloatField()
    lpg_kg = models.FloatField()

class Transportation(models.Model):
    emi_data = models.OneToOneField(EmissionData, on_delete=models.CASCADE, primary_key=True)
    distance_by_bus_km = models.FloatField()
    distance_by_personal_km = models.FloatField()
    distance_by_public_km = models.FloatField()
    distance_by_ev_km = models.FloatField()

class WaterUsage(models.Model):
    emi_data = models.OneToOneField(EmissionData, on_delete=models.CASCADE, primary_key=True)
    water_consumed_kl = models.FloatField()
    wastewater_treated_kl = models.FloatField()

class WasteManagement(models.Model):
    emi_data = models.OneToOneField(EmissionData, on_delete=models.CASCADE, primary_key=True)
    organic_waste_kg = models.FloatField()
    plastic_waste_kg = models.FloatField()
    sewage_liters = models.FloatField()