from django.contrib.auth.models import User
from django.db import models

class EmissionFactor(models.Model):
    category = models.CharField(max_length=100)
    factor = models.FloatField()

    def __str__(self):
        return self.category

class CollegeDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    total_campus_area = models.FloatField()
    total_builtup_area = models.FloatField()
    lawn_garden_area = models.FloatField()
    undeveloped_land_area = models.FloatField()

    def __str__(self):
        return self.name

class YearlyData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.year}"

class EnergyConsumption(models.Model):
    yearly_data = models.ForeignKey(YearlyData, on_delete=models.CASCADE)
    electricity_kwh = models.FloatField()
    solar_generation_kwh = models.FloatField()
    generator_fuel_liters = models.FloatField()

    def __str__(self):
        return str(self.yearly_data.year)

class Transportation(models.Model):
    yearly_data = models.ForeignKey(YearlyData, on_delete=models.CASCADE)
    total_students_staff = models.IntegerField()
    distance_by_bus_km = models.FloatField()
    distance_by_personal_vehicles_km = models.FloatField()
    distance_by_public_transport_km = models.FloatField()
    distance_by_ev_km = models.FloatField()

    def __str__(self):
        return str(self.yearly_data.year)

class WaterUsage(models.Model):
    yearly_data = models.ForeignKey(YearlyData, on_delete=models.CASCADE)
    water_consumed_kl = models.FloatField()
    rainwater_harvesting_capacity = models.FloatField()
    wastewater_treated_kl = models.FloatField()

    def __str__(self):
        return str(self.yearly_data.year)

class WasteManagement(models.Model):
    yearly_data = models.ForeignKey(YearlyData, on_delete=models.CASCADE)
    waste_generated_tonnes = models.FloatField()
    waste_treated_tonnes = models.FloatField()
    waste_to_landfill_tonnes = models.FloatField()

    def __str__(self):
        return str(self.yearly_data.year)