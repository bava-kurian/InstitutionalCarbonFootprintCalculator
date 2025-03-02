from django.db import models
from user.models import User

class MonthlyData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    electricity_kwh = models.FloatField(default=0.0)
    solar_generation_kwh = models.FloatField(default=0.0)
    generator_fuel_liters = models.FloatField(default=0.0)
    diesel_liters = models.FloatField(default=0.0)
    petrol_liters = models.FloatField(default=0.0)
    lpg_kg = models.FloatField(default=0.0)
    distance_by_bus_km = models.FloatField(default=0.0)
    distance_by_personal_km = models.FloatField(default=0.0)
    distance_by_public_km = models.FloatField(default=0.0)
    distance_by_ev_km = models.FloatField(default=0.0)
    water_consumed_kl = models.FloatField(default=0.0)
    wastewater_treated_kl = models.FloatField(default=0.0)
    organic_waste_kg = models.FloatField(default=0.0)
    plastic_waste_kg = models.FloatField(default=0.0)
    sewage_liters = models.FloatField(default=0.0)
    ewaste_kg = models.FloatField(default=0.0)
    paper_kg = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('user', 'year', 'month')

    def __str__(self):
        return f"{self.user.username} - {self.year}/{self.month}"
