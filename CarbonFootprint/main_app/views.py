from django.shortcuts import render, redirect
from .models import YearlyData,EmissionFactor, CollegeDetails, EnergyConsumption, Transportation, WaterUsage, WasteManagement
from .forms import EnergyConsumptionForm, TransportationForm, WaterUsageForm, WasteManagementForm
from .utils import calculate_emissions
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    yearly_data = YearlyData.objects.filter(user=request.user)
    energy_data = EnergyConsumption.objects.filter(yearly_data__in=yearly_data)
    transportation_data = Transportation.objects.filter(yearly_data__in=yearly_data)
    water_data = WaterUsage.objects.filter(yearly_data__in=yearly_data)
    waste_data = WasteManagement.objects.filter(yearly_data__in=yearly_data)

    context = {
        'yearly_data': yearly_data,
        'energy_data': energy_data,
        'transportation_data': transportation_data,
        'water_data': water_data,
        'waste_data': waste_data,
    }

    return render(request, 'main_app/home.html', context)


@login_required
def input_data(request):
    if request.method == 'POST':
        year = request.POST.get('year')
        yearly_data, created = YearlyData.objects.get_or_create(user=request.user, year=year)
        energy_form = EnergyConsumptionForm(request.POST)
        transportation_form = TransportationForm(request.POST)
        water_form = WaterUsageForm(request.POST)
        waste_form = WasteManagementForm(request.POST)
        if all([energy_form.is_valid(), transportation_form.is_valid(), water_form.is_valid(), waste_form.is_valid()]):
            energy = energy_form.save(commit=False)
            energy.yearly_data = yearly_data
            energy.save()
            transportation = transportation_form.save(commit=False)
            transportation.yearly_data = yearly_data
            transportation.save()
            water = water_form.save(commit=False)
            water.yearly_data = yearly_data
            water.save()
            waste = waste_form.save(commit=False)
            waste.yearly_data = yearly_data
            waste.save()
            return redirect('results_view')
    else:
        energy_form = EnergyConsumptionForm()
        transportation_form = TransportationForm()
        water_form = WaterUsageForm()
        waste_form = WasteManagementForm()
    return render(request, 'main_app/input_form.html', {
        'energy_form': energy_form,
        'transportation_form': transportation_form,
        'water_form': water_form,
        'waste_form': waste_form,
    })
def calculate_emissions_view(request):
    year = request.POST.get('year')
    print("Year:", year)  # Print the year being fetched

    energy_data = EnergyConsumption.objects.filter(year=year).first()
    transportation_data = Transportation.objects.filter(year=year).first()
    water_data = WaterUsage.objects.filter(year=year).first()
    waste_data = WasteManagement.objects.filter(year=year).first()

    print("Energy Data:", energy_data)  # Print the fetched energy data
    print("Transportation Data:", transportation_data)  # Print the fetched transportation data
    print("Water Data:", water_data)  # Print the fetched water data
    print("Waste Data:", waste_data)  # Print the fetched waste data

    data = {
        'energy': energy_data,
        'transportation': transportation_data,
        'water': water_data,
        'waste': waste_data
    }

    emissions = calculate_emissions(data)
    print("Emissions:", emissions)  # Print the calculated emissions

    # Exclude the total emissions from the chart data
    chart_data = {k: v for k, v in emissions.items() if k != 'total'}

    return render(request, 'main_app/results.html', {'emissions': emissions, 'chart_data': chart_data})
def results_view(request):
    print("Data:")
    return render(request, 'main_app/results.html')