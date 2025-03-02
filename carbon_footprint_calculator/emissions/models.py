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
    ewaste=models.FloatField(default=0.0)
    refrigerant_gwp = models.FloatField()

    def __str__(self):
        return f"Emission Factors"

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
    paper_emissions = models.FloatField(default=0.0)
    ewaste_emissions = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('user', 'year')

    def __str__(self):
        return f"{self.user.username} - {self.year}"

class EnergyConsumption(models.Model):
    emi_data = models.OneToOneField(EmissionData, on_delete=models.CASCADE, primary_key=True)
    electricity_kwh = models.FloatField()
    solar_generation_kwh = models.FloatField()
    generator_fuel_liters = models.FloatField()

    def __str__(self):
        return f"Energy Consumption for {self.emi_data.year}"

class FuelConsumption(models.Model):
    emi_data = models.OneToOneField(EmissionData, on_delete=models.CASCADE, primary_key=True)
    diesel_liters = models.FloatField()
    petrol_liters = models.FloatField()
    lpg_kg = models.FloatField()

    def __str__(self):
        return f"Fuel Consumption for {self.emi_data.year}"

class Transportation(models.Model):
    emi_data = models.OneToOneField(EmissionData, on_delete=models.CASCADE, primary_key=True)
    distance_by_bus_km = models.FloatField()
    distance_by_personal_km = models.FloatField()
    distance_by_public_km = models.FloatField()
    distance_by_ev_km = models.FloatField()

    def __str__(self):
        return f"Transportation for {self.emi_data.year}"

class WaterUsage(models.Model):
    emi_data = models.OneToOneField(EmissionData, on_delete=models.CASCADE, primary_key=True)
    water_consumed_kl = models.FloatField()
    wastewater_treated_kl = models.FloatField()

    def __str__(self):
        return f"Water Usage for {self.emi_data.year}"

class WasteManagement(models.Model):
    emi_data = models.OneToOneField(EmissionData, on_delete=models.CASCADE, primary_key=True)
    organic_waste_kg = models.FloatField()
    plastic_waste_kg = models.FloatField()
    sewage_liters = models.FloatField()
    ewaste_kg = models.FloatField()

    def __str__(self):
        return f"Waste Management for {self.emi_data.year}"

class PaperUsage(models.Model):
    emi_data = models.OneToOneField(EmissionData, on_delete=models.CASCADE, primary_key=True)
    paper_kg = models.FloatField()

    def __str__(self):
        return f"Paper Usage for {self.emi_data.year}"

class MonthlyEmissionData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    is_complete = models.BooleanField(default=False)
    
    # Energy
    electricity_kwh = models.FloatField(null=True, blank=True, default=None)
    solar_generation_kwh = models.FloatField(null=True, blank=True, default=None)
    generator_fuel_liters = models.FloatField(null=True, blank=True, default=None)
    
    # Fuel
    diesel_liters = models.FloatField(null=True, blank=True, default=None)
    petrol_liters = models.FloatField(null=True, blank=True, default=None)
    lpg_kg = models.FloatField(null=True, blank=True, default=None)
    
    # Transportation
    distance_by_bus_km = models.FloatField(null=True, blank=True, default=None)
    distance_by_personal_km = models.FloatField(null=True, blank=True, default=None)
    distance_by_public_km = models.FloatField(null=True, blank=True, default=None)
    distance_by_ev_km = models.FloatField(null=True, blank=True, default=None)
    
    # Water
    water_consumed_kl = models.FloatField(null=True, blank=True, default=None)
    wastewater_treated_kl = models.FloatField(null=True, blank=True, default=None)
    
    # Waste
    organic_waste_kg = models.FloatField(null=True, blank=True, default=None)
    plastic_waste_kg = models.FloatField(null=True, blank=True, default=None)
    sewage_liters = models.FloatField(null=True, blank=True, default=None)
    ewaste_kg = models.FloatField(null=True, blank=True, default=None)
    
    # Paper
    paper_kg = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        unique_together = ('user', 'year', 'month')
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(year__lt=models.F('year')),
                name='one_year_per_user'
            )
        ]