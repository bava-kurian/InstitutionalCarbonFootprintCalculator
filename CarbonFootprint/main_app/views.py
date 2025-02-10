from django.shortcuts import render, redirect,HttpResponse
from .models import EmissionFactor, CollegeDetails, EnergyConsumption, Transportation, WaterUsage, WasteManagement
from .forms import EnergyConsumptionForm, TransportationForm, WaterUsageForm, WasteManagementForm
from .utils import calculate_emissions
from django.contrib.auth.decorators import login_required


def base_view(request):
    return render(request, 'main_app/base.html');
def home(request):
    energy_data = EnergyConsumption.objects.filter(user=request.user)
    transportation_data = Transportation.objects.filter(user=request.user)
    water_data = WaterUsage.objects.filter(user=request.user)
    waste_data = WasteManagement.objects.filter(user=request.user)

    context = {
        'energy_data': energy_data,
        'transportation_data': transportation_data,
        'water_data': water_data,
        'waste_data': waste_data,
    }

    return render(request, 'main_app/home.html', context)
@login_required
def input_data(request):
    if request.method == 'POST':
        print("POST data:", request.POST)  # Print the posted data
        energy_form = EnergyConsumptionForm(request.POST)
        transportation_form = TransportationForm(request.POST)
        water_form = WaterUsageForm(request.POST)
        waste_form = WasteManagementForm(request.POST)
        if all([energy_form.is_valid(), transportation_form.is_valid(), water_form.is_valid(), waste_form.is_valid()]):
            energy_form.save()
            transportation_form.save()
            water_form.save()
            waste_form.save()
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
        'year': 2025  # Replace with the actual year you want to use
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