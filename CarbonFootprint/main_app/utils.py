from .models import EmissionFactor

def calculate_emissions(data):
    emissions = {}
    total_emissions = 0

    # Calculate energy emissions
    energy_factors = EmissionFactor.objects.filter(category='energy').first()
    if data['energy'] and energy_factors:
        energy_emissions = data['energy'].electricity_kwh * energy_factors.factor
    else:
        energy_emissions = 0
    emissions['energy'] = energy_emissions
    total_emissions += energy_emissions

    # Calculate transportation emissions
    transportation_factors = EmissionFactor.objects.filter(category='transportation').first()
    if data['transportation'] and transportation_factors:
        transportation_emissions = data['transportation'].distance_by_bus_km * transportation_factors.factor
    else:
        transportation_emissions = 0
    emissions['transportation'] = transportation_emissions
    total_emissions += transportation_emissions

    # Calculate water emissions
    water_factors = EmissionFactor.objects.filter(category='water').first()
    if data['water'] and water_factors:
        water_emissions = data['water'].water_consumed_kl * water_factors.factor
    else:
        water_emissions = 0
    emissions['water'] = water_emissions
    total_emissions += water_emissions

    # Calculate waste emissions
    waste_factors = EmissionFactor.objects.filter(category='waste').first()
    if data['waste'] and waste_factors:
        waste_emissions = data['waste'].waste_generated_tonnes * waste_factors.factor
    else:
        waste_emissions = 0
    emissions['waste'] = waste_emissions
    total_emissions += waste_emissions

    emissions['total'] = total_emissions
    return emissions