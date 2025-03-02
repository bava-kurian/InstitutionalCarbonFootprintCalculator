from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import EmissionData, EmissionFactor, EnergyConsumption, FuelConsumption, Transportation, WaterUsage, WasteManagement, PaperUsage
from .forms import EmissionDataForm, EnergyConsumptionForm, FuelConsumptionForm, TransportationForm, WaterUsageForm, WasteManagementForm, PaperUsageForm
import csv
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime

@login_required
def input_data(request):
    year = request.GET.get('year')
    if year:
        emission_data = get_object_or_404(EmissionData, user=request.user, year=year)
        energy = get_object_or_404(EnergyConsumption, emi_data=emission_data)
        fuel = get_object_or_404(FuelConsumption, emi_data=emission_data)
        transport = get_object_or_404(Transportation, emi_data=emission_data)
        water = get_object_or_404(WaterUsage, emi_data=emission_data)
        waste = get_object_or_404(WasteManagement, emi_data=emission_data)
        paper = get_object_or_404(PaperUsage, emi_data=emission_data)
    else:
        emission_data = None
        energy = None
        fuel = None
        transport = None
        water = None
        waste = None
        paper = None

    if request.method == 'POST':
        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                return HttpResponse("Please upload a valid CSV file.")
            
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                if row['year'] == year:
                    emi_data_form = EmissionDataForm({
                        'year': row['year'],
                        'user': request.user.id
                    }, instance=emission_data)
                    energy_form = EnergyConsumptionForm({
                        'electricity_kwh': row['electricity_kwh'],
                        'solar_generation_kwh': row['solar_generation_kwh'],
                        'generator_fuel_liters': row['generator_fuel_liters']
                    }, instance=energy)
                    fuel_form = FuelConsumptionForm({
                        'diesel_liters': row['diesel_liters'],
                        'petrol_liters': row['petrol_liters'],
                        'lpg_kg': row['lpg_kg']
                    }, instance=fuel)
                    transport_form = TransportationForm({
                        'distance_by_bus_km': row['distance_by_bus_km'],
                        'distance_by_personal_km': row['distance_by_personal_km'],
                        'distance_by_public_km': row['distance_by_public_km'],
                        'distance_by_ev_km': row['distance_by_ev_km']
                    }, instance=transport)
                    water_form = WaterUsageForm({
                        'water_consumed_kl': row['water_consumed_kl'],
                        'wastewater_treated_kl': row['wastewater_treated_kl']
                    }, instance=water)
                    waste_form = WasteManagementForm({
                        'organic_waste_kg': row['organic_waste_kg'],
                        'plastic_waste_kg': row['plastic_waste_kg'],
                        'sewage_liters': row['sewage_liters'],
                        'ewaste_kg': row['ewaste_kg']
                    }, instance=waste)
                    paper_form = PaperUsageForm({
                        'paper_kg': row['paper_kg']
                    }, instance=paper)
                    break
        else:
            emi_data_form = EmissionDataForm(request.POST, instance=emission_data)
            energy_form = EnergyConsumptionForm(request.POST, instance=energy)
            fuel_form = FuelConsumptionForm(request.POST, instance=fuel)
            transport_form = TransportationForm(request.POST, instance=transport)
            water_form = WaterUsageForm(request.POST, instance=water)
            waste_form = WasteManagementForm(request.POST, instance=waste)
            paper_form = PaperUsageForm(request.POST, instance=paper)

        if (emi_data_form.is_valid() and energy_form.is_valid() and fuel_form.is_valid() and
            transport_form.is_valid() and water_form.is_valid() and waste_form.is_valid() and paper_form.is_valid()):
            
            emission_data = emi_data_form.save(commit=False)
            emission_data.user = request.user
            if EmissionData.objects.filter(user=request.user, year=emission_data.year).exclude(pk=emission_data.pk).exists():
                emi_data_form.add_error('year', 'You have already entered data for this year.')
            else:
                emission_data.save()
                energy = energy_form.save(commit=False)
                energy.emi_data = emission_data
                energy.electricity_kwh = sum([float(request.POST.get(f'electricity_kwh_{i}', 0)) for i in range(1, 13)])
                energy.save()
                fuel = fuel_form.save(commit=False)
                fuel.emi_data = emission_data
                fuel.diesel_liters = sum([float(request.POST.get(f'diesel_liters_{i}', 0)) for i in range(1, 13)])
                fuel.save()
                transport = transport_form.save(commit=False)
                transport.emi_data = emission_data
                transport.save()
                water = water_form.save(commit=False)
                water.emi_data = emission_data
                water.save()
                waste = waste_form.save(commit=False)
                waste.emi_data = emission_data
                waste.save()
                paper = paper_form.save(commit=False)
                paper.emi_data = emission_data
                paper.save()
                return redirect('results', emission_data.id)
    else:
        emi_data_form = EmissionDataForm(instance=emission_data)
        energy_form = EnergyConsumptionForm(instance=energy)
        fuel_form = FuelConsumptionForm(instance=fuel)
        transport_form = TransportationForm(instance=transport)
        water_form = WaterUsageForm(instance=water)
        waste_form = WasteManagementForm(instance=waste)
        paper_form = PaperUsageForm(instance=paper)

    return render(request, 'emissions/input_form.html', {
        'emi_data_form': emi_data_form,
        'energy_form': energy_form,
        'fuel_form': fuel_form,
        'transport_form': transport_form,
        'water_form': water_form,
        'waste_form': waste_form,
        'paper_form': paper_form,
    })

@login_required
def edit_data(request, emi_data_id):
    emission_data = get_object_or_404(EmissionData, pk=emi_data_id, user=request.user)
    energy = get_object_or_404(EnergyConsumption, emi_data=emission_data)
    fuel = get_object_or_404(FuelConsumption, emi_data=emission_data)
    transport = get_object_or_404(Transportation, emi_data=emission_data)
    water = get_object_or_404(WaterUsage, emi_data=emission_data)
    waste = get_object_or_404(WasteManagement, emi_data=emission_data)
    paper = get_object_or_404(PaperUsage, emi_data=emission_data)

    if request.method == 'POST':
        emi_data_form = EmissionDataForm(request.POST, instance=emission_data)
        energy_form = EnergyConsumptionForm(request.POST, instance=energy)
        fuel_form = FuelConsumptionForm(request.POST, instance=fuel)
        transport_form = TransportationForm(request.POST, instance=transport)
        water_form = WaterUsageForm(request.POST, instance=water)
        waste_form = WasteManagementForm(request.POST, instance=waste)
        paper_form = PaperUsageForm(request.POST, instance=paper)

        if (emi_data_form.is_valid() and energy_form.is_valid() and fuel_form.is_valid() and
            transport_form.is_valid() and water_form.is_valid() and waste_form.is_valid() and paper_form.is_valid()):
            
            emission_data = emi_data_form.save(commit=False)
            emission_data.user = request.user
            emission_data.save()
            energy = energy_form.save(commit=False)
            energy.emi_data = emission_data
            energy.electricity_kwh = sum([float(request.POST.get(f'electricity_kwh_{i}', 0)) for i in range(1, 13)])
            energy.save()
            fuel = fuel_form.save(commit=False)
            fuel.emi_data = emission_data
            fuel.diesel_liters = sum([float(request.POST.get(f'diesel_liters_{i}', 0)) for i in range(1, 13)])
            fuel.save()
            transport = transport_form.save(commit=False)
            transport.emi_data = emission_data
            transport.save()
            water = water_form.save(commit=False)
            water.emi_data = emission_data
            water.save()
            waste = waste_form.save(commit=False)
            waste.emi_data = emission_data
            waste.save()
            paper = paper_form.save(commit=False)
            paper.emi_data = emission_data
            paper.save()
            return redirect('results', emission_data.id)
    else:
        emi_data_form = EmissionDataForm(instance=emission_data)
        energy_form = EnergyConsumptionForm(instance=energy)
        fuel_form = FuelConsumptionForm(instance=fuel)
        transport_form = TransportationForm(instance=transport)
        water_form = WaterUsageForm(instance=water)
        waste_form = WasteManagementForm(instance=waste)
        paper_form = PaperUsageForm(instance=paper)

    return render(request, 'emissions/edit_form.html', {
        'emi_data_form': emi_data_form,
        'energy_form': energy_form,
        'fuel_form': fuel_form,
        'transport_form': transport_form,
        'water_form': water_form,
        'waste_form': waste_form,
        'paper_form': paper_form,
    })

@login_required
def results(request, emi_data_id):
    emission_data = get_object_or_404(EmissionData, pk=emi_data_id)
    current_year = datetime.now().year

    # Ensure there is at least one EmissionFactor entry
    factors = EmissionFactor.objects.first()
    if not factors:
        # Optionally, you can create a default EmissionFactor entry here or handle the error
        factors = EmissionFactor.objects.create(
            electricity=0.5, diesel=2.68, petrol=2.31, lpg=1.5, water_supply=0.344,
            wastewater_treatment=0.2, organic_waste=0.1, plastic_waste=6.0,
            sewage_treatment=0.3, paper=1.5, refrigerant_gwp=1000,ewaste=1.0,
        )

    energy = emission_data.energyconsumption
    fuel = emission_data.fuelconsumption
    transport = emission_data.transportation
    water = emission_data.waterusage
    waste = emission_data.wastemanagement
    paper = emission_data.paperusage

    electricity_emissions = energy.electricity_kwh * factors.electricity
    diesel_emissions = fuel.diesel_liters * 2.68
    petrol_emissions = fuel.petrol_liters * 2.31
    lpg_emissions = fuel.lpg_kg * factors.lpg
    public_transport_emissions = transport.distance_by_public_km * 0.125
    water_supply_emissions = water.water_consumed_kl * 0.344
    plastic_waste_emissions = waste.plastic_waste_kg * 6.0
    paper_emissions = paper.paper_kg * factors.paper
    ewaste_emissions = waste.ewaste_kg * factors.ewaste

    total_emissions = (
        electricity_emissions + diesel_emissions + petrol_emissions +
        lpg_emissions + public_transport_emissions + water_supply_emissions +
        plastic_waste_emissions + paper_emissions
    )

    emission_data.total_emissions = total_emissions
    emission_data.electricity_emissions = electricity_emissions
    emission_data.diesel_emissions = diesel_emissions
    emission_data.petrol_emissions = petrol_emissions
    emission_data.lpg_emissions = lpg_emissions
    emission_data.public_transport_emissions = public_transport_emissions
    emission_data.water_supply_emissions = water_supply_emissions
    emission_data.plastic_waste_emissions = plastic_waste_emissions
    emission_data.paper_emissions = paper_emissions
    emission_data.ewaste_emissions = ewaste_emissions
    emission_data.save()

    context = {
        'emission_data': emission_data,
        'electricity_emissions': electricity_emissions,
        'diesel_emissions': diesel_emissions,
        'petrol_emissions': petrol_emissions,
        'lpg_emissions': lpg_emissions,
        'public_transport_emissions': public_transport_emissions,
        'water_supply_emissions': water_supply_emissions,
        'plastic_waste_emissions': plastic_waste_emissions,
        'paper_emissions': paper_emissions,
        'total_emissions': total_emissions,
        'current_year': current_year,
        'ewaste_emissions': emission_data.ewaste_emissions,
    }
    return render(request, 'emissions/results.html', context)

@login_required
def download_pdf(request, emi_data_id):
    emission_data = get_object_or_404(EmissionData, pk=emi_data_id)
    context = {
        'emission_data': emission_data,
        'electricity_emissions': emission_data.electricity_emissions,
        'diesel_emissions': emission_data.diesel_emissions,
        'petrol_emissions': emission_data.petrol_emissions,
        'lpg_emissions': emission_data.lpg_emissions,
        'public_transport_emissions': emission_data.public_transport_emissions,
        'water_supply_emissions': emission_data.water_supply_emissions,
        'plastic_waste_emissions': emission_data.plastic_waste_emissions,
        'paper_emissions': emission_data.paper_emissions,
        'total_emissions': emission_data.total_emissions,
        'ewaste_emissions': emission_data.ewaste_emissions,
    }
    template_path = 'emissions/pdf_template.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="emission_report_{emission_data.year}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required
def emission_detail(request, emi_data_id):
    emission_data = get_object_or_404(EmissionData, pk=emi_data_id, user=request.user)
    energy = emission_data.energyconsumption
    fuel = emission_data.fuelconsumption
    transport = emission_data.transportation
    water = emission_data.waterusage
    waste = emission_data.wastemanagement
    paper = emission_data.paperusage

    context = {
        'emission_data': emission_data,
        'energy': energy,
        'fuel': fuel,
        'transport': transport,
        'water': water,
        'waste': waste,
        'paper': paper,
    }
    return render(request, 'emissions/emission_detail.html', context)