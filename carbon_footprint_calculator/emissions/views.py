from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import EmissionData, EmissionFactor, EnergyConsumption, FuelConsumption, Transportation, WaterUsage, WasteManagement, PaperUsage, FoodConsumption, Refrigerants
from .forms import EmissionDataForm, EnergyConsumptionForm, FuelConsumptionForm, TransportationForm, WaterUsageForm, WasteManagementForm, PaperUsageForm, FoodConsumptionForm, RefrigerantsForm
import csv
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime
from django.db.models import Sum
from .models import MonthlyEmissionData
from urllib.parse import urlencode

@login_required
def check_year(request):
    year = request.GET.get('year')
    exists = EmissionData.objects.filter(
        user=request.user,
        year=year
    ).exists()
    return JsonResponse({'exists': exists})

@login_required
def input_data(request):
    year_error = None
    if request.method == 'POST':
        year = request.POST.get('year')
        if EmissionData.objects.filter(user=request.user, year=year).exists():
            year_error = f"Data for year {year} already exists. Please choose a different year."
            return render(request, 'emissions/input_form.html', {
                'year_error': year_error,
                'emi_data_form': EmissionDataForm(request.POST),
                'energy_form': EnergyConsumptionForm(request.POST),
                'fuel_form': FuelConsumptionForm(request.POST),
                'transport_form': TransportationForm(request.POST),
                'water_form': WaterUsageForm(request.POST),
                'waste_form': WasteManagementForm(request.POST),
                'paper_form': PaperUsageForm(request.POST),
                'food_form': FoodConsumptionForm(request.POST),
                'refrigerants_form': RefrigerantsForm(request.POST)
            })
        # Create a new EmissionData instance for the submitted data
        emi_data_form = EmissionDataForm(request.POST)
        energy_form = EnergyConsumptionForm(request.POST)
        fuel_form = FuelConsumptionForm(request.POST)
        transport_form = TransportationForm(request.POST)
        water_form = WaterUsageForm(request.POST)
        waste_form = WasteManagementForm(request.POST)
        paper_form = PaperUsageForm(request.POST)
        food_form = FoodConsumptionForm(request.POST)
        refrigerants_form = RefrigerantsForm(request.POST)

        if (emi_data_form.is_valid() and energy_form.is_valid() and fuel_form.is_valid() and
            transport_form.is_valid() and water_form.is_valid() and waste_form.is_valid() and paper_form.is_valid() and
            food_form.is_valid() and refrigerants_form.is_valid()):
            
            emission_data = emi_data_form.save(commit=False)
            emission_data.user = request.user
            emission_data.save()

            energy = energy_form.save(commit=False)
            energy.emi_data = emission_data
            energy.save()

            fuel = fuel_form.save(commit=False)
            fuel.emi_data = emission_data
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

            food = food_form.save(commit=False)
            food.emi_data = emission_data
            food.save()

            refrigerants = refrigerants_form.save(commit=False)
            refrigerants.emi_data = emission_data
            refrigerants.save()

            return redirect('results', emission_data.id)
    else:
        year = request.GET.get('year')
        
        # Initialize all forms
        emi_data_form = EmissionDataForm()
        energy_form = EnergyConsumptionForm()
        fuel_form = FuelConsumptionForm()
        transport_form = TransportationForm()
        water_form = WaterUsageForm()
        waste_form = WasteManagementForm()
        paper_form = PaperUsageForm()
        food_form = FoodConsumptionForm()  # Initialize this
        refrigerants_form = RefrigerantsForm()  # Initialize this
        
        # Check if we have prefilled data from monthly summary
        prefilled_data = {
            'year': year,
            'electricity_kwh': request.GET.get('electricity_kwh'),
            'solar_generation_kwh': request.GET.get('solar_generation_kwh'),
            'generator_fuel_liters': request.GET.get('generator_fuel_liters'),
            'diesel_liters': request.GET.get('diesel_liters'),
            'petrol_liters': request.GET.get('petrol_liters'),
            'lpg_kg': request.GET.get('lpg_kg'),
            'distance_by_bus_km': request.GET.get('distance_by_bus_km'),
            'distance_by_personal_km': request.GET.get('distance_by_personal_km'),
            'distance_by_public_km': request.GET.get('distance_by_public_km'),
            'distance_by_ev_km': request.GET.get('distance_by_ev_km'),
            'water_consumed_kl': request.GET.get('water_consumed_kl'),
            'wastewater_treated_kl': request.GET.get('wastewater_treated_kl'),
            'organic_waste_kg': request.GET.get('organic_waste_kg'),
            'plastic_waste_kg': request.GET.get('plastic_waste_kg'),
            'sewage_liters': request.GET.get('sewage_liters'),
            'ewaste_kg': request.GET.get('ewaste_kg'),
            'paper_kg': request.GET.get('paper_kg'),
            'red_meat_kg': request.GET.get('red_meat_kg'),
            'poultry_kg': request.GET.get('poultry_kg'),
            'vegetables_kg': request.GET.get('vegetables_kg'),
            'r134a_kg': request.GET.get('r134a_kg'),
            'r410a_kg': request.GET.get('r410a_kg')
        }
        
        if year and all(v is not None for v in prefilled_data.values()):
            emi_data_form = EmissionDataForm(initial={'year': year})
            energy_form = EnergyConsumptionForm(initial={
                'electricity_kwh': prefilled_data['electricity_kwh'],
                'solar_generation_kwh': prefilled_data['solar_generation_kwh'],
                'generator_fuel_liters': prefilled_data['generator_fuel_liters']
            })
            fuel_form = FuelConsumptionForm(initial={
                'diesel_liters': prefilled_data['diesel_liters'],
                'petrol_liters': prefilled_data['petrol_liters'],
                'lpg_kg': prefilled_data['lpg_kg']
            })
            transport_form = TransportationForm(initial={
                'distance_by_bus_km': prefilled_data['distance_by_bus_km'],
                'distance_by_personal_km': prefilled_data['distance_by_personal_km'],
                'distance_by_public_km': prefilled_data['distance_by_public_km'],
                'distance_by_ev_km': prefilled_data['distance_by_ev_km']
            })
            water_form = WaterUsageForm(initial={
                'water_consumed_kl': prefilled_data['water_consumed_kl'],
                'wastewater_treated_kl': prefilled_data['wastewater_treated_kl']
            })
            waste_form = WasteManagementForm(initial={
                'organic_waste_kg': prefilled_data['organic_waste_kg'],
                'plastic_waste_kg': prefilled_data['plastic_waste_kg'],
                'sewage_liters': prefilled_data['sewage_liters'],
                'ewaste_kg': prefilled_data['ewaste_kg']
            })
            paper_form = PaperUsageForm(initial={
                'paper_kg': prefilled_data['paper_kg']
            })
            food_form = FoodConsumptionForm(initial={
                'red_meat_kg': prefilled_data['red_meat_kg'],
                'poultry_kg': prefilled_data['poultry_kg'],
                'vegetables_kg': prefilled_data['vegetables_kg']
            })
            refrigerants_form = RefrigerantsForm(initial={
                'r134a_kg': prefilled_data['r134a_kg'],
                'r410a_kg': prefilled_data['r410a_kg']
            })
        else:
            if year:
                emission_data = get_object_or_404(EmissionData, user=request.user, year=year)
                energy = get_object_or_404(EnergyConsumption, emi_data=emission_data)
                fuel = get_object_or_404(FuelConsumption, emi_data=emission_data)
                transport = get_object_or_404(Transportation, emi_data=emission_data)
                water = get_object_or_404(WaterUsage, emi_data=emission_data)
                waste = get_object_or_404(WasteManagement, emi_data=emission_data)
                paper = get_object_or_404(PaperUsage, emi_data=emission_data)
                food = get_object_or_404(FoodConsumption, emi_data=emission_data)  # Add this
                refrigerants = get_object_or_404(Refrigerants, emi_data=emission_data)  # Add this
            else:
                emission_data = None
                energy = None
                fuel = None
                transport = None
                water = None
                waste = None
                paper = None
                food = None  # Add this
                refrigerants = None  # Add this

            if request.method == 'POST':
                if 'csv_file' in request.FILES:
                    csv_file = request.FILES['csv_file']
                    if not csv_file.name.endswith('.csv'):
                        return HttpResponse("Please upload a valid CSV file.")
                    
                    decoded_file = csv_file.read().decode('utf-8').splitlines()
                    reader = csv.DictReader(decoded_file)
                    for row in reader:
                        # Initialize all forms with CSV data
                        emi_data_form = EmissionDataForm({
                            'year': row['year'],
                            'user': request.user.id
                        })
                        energy_form = EnergyConsumptionForm({
                            'electricity_kwh': row['electricity_kwh'],
                            'solar_generation_kwh': row['solar_generation_kwh'],
                            'generator_fuel_liters': row['generator_fuel_liters']
                        })
                        fuel_form = FuelConsumptionForm({
                            'diesel_liters': row['diesel_liters'],
                            'petrol_liters': row['petrol_liters'],
                            'lpg_kg': row['lpg_kg']
                        })
                        transport_form = TransportationForm({
                            'distance_by_bus_km': row['distance_by_bus_km'],
                            'distance_by_personal_km': row['distance_by_personal_km'],
                            'distance_by_public_km': row['distance_by_public_km'],
                            'distance_by_ev_km': row['distance_by_ev_km']
                        })
                        water_form = WaterUsageForm({
                            'water_consumed_kl': row['water_consumed_kl'],
                            'wastewater_treated_kl': row['wastewater_treated_kl']
                        })
                        waste_form = WasteManagementForm({
                            'organic_waste_kg': row['organic_waste_kg'],
                            'plastic_waste_kg': row['plastic_waste_kg'],
                            'sewage_liters': row['sewage_liters'],
                            'ewaste_kg': row['ewaste_kg']
                        })
                        paper_form = PaperUsageForm({
                            'paper_kg': row['paper_kg']
                        })
                        food_form = FoodConsumptionForm({
                            'red_meat_kg': row['red_meat_kg'],
                            'poultry_kg': row['poultry_kg'],
                            'vegetables_kg': row['vegetables_kg']
                        })
                        refrigerants_form = RefrigerantsForm({
                            'r134a_kg': row['r134a_kg'],
                            'r410a_kg': row['r410a_kg']
                        })

                        # Process the forms normally
                        if (emi_data_form.is_valid() and energy_form.is_valid() and fuel_form.is_valid() and
                            transport_form.is_valid() and water_form.is_valid() and waste_form.is_valid() and paper_form.is_valid() and
                            food_form.is_valid() and refrigerants_form.is_valid()):
                            
                            emission_data = emi_data_form.save(commit=False)
                            emission_data.user = request.user
                            emission_data.save()

                            energy = energy_form.save(commit=False)
                            energy.emi_data = emission_data
                            energy.save()

                            fuel = fuel_form.save(commit=False)
                            fuel.emi_data = emission_data
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

                            food = food_form.save(commit=False)
                            food.emi_data = emission_data
                            food.save()

                            refrigerants = refrigerants_form.save(commit=False)
                            refrigerants.emi_data = emission_data
                            refrigerants.save()

                            return redirect('results', emission_data.id)
                else:
                    emi_data_form = EmissionDataForm(request.POST, instance=emission_data)
                    energy_form = EnergyConsumptionForm(request.POST, instance=energy)
                    fuel_form = FuelConsumptionForm(request.POST, instance=fuel)
                    transport_form = TransportationForm(request.POST, instance=transport)
                    water_form = WaterUsageForm(request.POST, instance=water)
                    waste_form = WasteManagementForm(request.POST, instance=waste)
                    paper_form = PaperUsageForm(request.POST, instance=paper)
                    food_form = FoodConsumptionForm(request.POST, instance=food)  # Add this
                    refrigerants_form = RefrigerantsForm(request.POST, instance=refrigerants)  # Add this

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
                        energy.save()
                        fuel = fuel_form.save(commit=False)
                        fuel.emi_data = emission_data
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
                food_form = FoodConsumptionForm(instance=food)  # Add this
                refrigerants_form = RefrigerantsForm(instance=refrigerants)  # Add this

    return render(request, 'emissions/input_form.html', {
        'emi_data_form': emi_data_form,
        'energy_form': energy_form,
        'fuel_form': fuel_form,
        'transport_form': transport_form,
        'water_form': water_form,
        'waste_form': waste_form,
        'paper_form': paper_form,
        'food_form': food_form,           # Add this line
        'refrigerants_form': refrigerants_form  # Add this line
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
    food = get_object_or_404(FoodConsumption, emi_data=emission_data)
    refrigerants = get_object_or_404(Refrigerants, emi_data=emission_data)

    if request.method == 'POST':
        emi_data_form = EmissionDataForm(request.POST, instance=emission_data)
        energy_form = EnergyConsumptionForm(request.POST, instance=energy)
        fuel_form = FuelConsumptionForm(request.POST, instance=fuel)
        transport_form = TransportationForm(request.POST, instance=transport)
        water_form = WaterUsageForm(request.POST, instance=water)
        waste_form = WasteManagementForm(request.POST, instance=waste)
        paper_form = PaperUsageForm(request.POST, instance=paper)
        food_form = FoodConsumptionForm(request.POST, instance=food)
        refrigerants_form = RefrigerantsForm(request.POST, instance=refrigerants)

        if (emi_data_form.is_valid() and energy_form.is_valid() and fuel_form.is_valid() and
            transport_form.is_valid() and water_form.is_valid() and waste_form.is_valid() and paper_form.is_valid() and
            food_form.is_valid() and refrigerants_form.is_valid()):
            
            emission_data = emi_data_form.save(commit=False)
            emission_data.user = request.user
            emission_data.save()
            energy = energy_form.save(commit=False)
            energy.emi_data = emission_data
            energy.save()
            fuel = fuel_form.save(commit=False)
            fuel.emi_data = emission_data
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
            food = food_form.save(commit=False)
            food.emi_data = emission_data
            food.save()
            refrigerants = refrigerants_form.save(commit=False)
            refrigerants.emi_data = emission_data
            refrigerants.save()
            return redirect('results', emission_data.id)
    else:
        emi_data_form = EmissionDataForm(instance=emission_data)
        energy_form = EnergyConsumptionForm(instance=energy)
        fuel_form = FuelConsumptionForm(instance=fuel)
        transport_form = TransportationForm(instance=transport)
        water_form = WaterUsageForm(instance=water)
        waste_form = WasteManagementForm(instance=waste)
        paper_form = PaperUsageForm(instance=paper)
        food_form = FoodConsumptionForm(instance=food)
        refrigerants_form = RefrigerantsForm(instance=refrigerants)

    return render(request, 'emissions/edit_form.html', {
        'emi_data_form': emi_data_form,
        'energy_form': energy_form,
        'fuel_form': fuel_form,
        'transport_form': transport_form,
        'water_form': water_form,
        'waste_form': waste_form,
        'paper_form': paper_form,
        'food_form': food_form,           # Add this line
        'refrigerants_form': refrigerants_form  # Add this line
    })

@login_required
def results(request, emi_data_id):
    emission_data = get_object_or_404(EmissionData, pk=emi_data_id)
    current_year = datetime.now().year

    # Ensure there is at least one EmissionFactor entry
    factors = EmissionFactor.objects.first()

    energy = emission_data.energyconsumption
    fuel = emission_data.fuelconsumption
    transport = emission_data.transportation
    water = emission_data.waterusage
    waste = emission_data.wastemanagement
    paper = emission_data.paperusage
    food = emission_data.foodconsumption
    refrigerants = emission_data.refrigerants

    electricity_emissions = energy.electricity_kwh * factors.electricity
    diesel_emissions = fuel.diesel_liters * factors.diesel
    petrol_emissions = fuel.petrol_liters * factors.petrol
    lpg_emissions = fuel.lpg_kg * factors.lpg
    public_transport_emissions = transport.distance_by_public_km *factors.public_transport
    water_supply_emissions = water.water_consumed_kl * factors.water_supply
    plastic_waste_emissions = waste.plastic_waste_kg * factors.plastic_waste
    paper_emissions = paper.paper_kg * factors.paper
    ewaste_emissions = waste.ewaste_kg * factors.ewaste
    red_meat_emissions = food.red_meat_kg * factors.red_meat
    poultry_emissions = food.poultry_kg * factors.poultry
    vegetables_emissions = food.vegetables_kg * factors.vegetables
    r134a_emissions = refrigerants.r134a_kg * factors.r134a
    r410a_emissions = refrigerants.r410a_kg * factors.r410a

    total_emissions = (
        electricity_emissions + diesel_emissions + petrol_emissions +
        lpg_emissions + public_transport_emissions + water_supply_emissions +
        plastic_waste_emissions + paper_emissions + red_meat_emissions +
        poultry_emissions + vegetables_emissions + r134a_emissions + r410a_emissions
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
    emission_data.red_meat_emissions = red_meat_emissions
    emission_data.poultry_emissions = poultry_emissions
    emission_data.vegetables_emissions = vegetables_emissions
    emission_data.r134a_emissions = r134a_emissions
    emission_data.r410a_emissions = r410a_emissions
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
        'red_meat_emissions': red_meat_emissions,
        'poultry_emissions': poultry_emissions,
        'vegetables_emissions': vegetables_emissions,
        'r134a_emissions': r134a_emissions,
        'r410a_emissions': r410a_emissions,
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
        'red_meat_emissions': emission_data.red_meat_emissions,
        'poultry_emissions': emission_data.poultry_emissions,
        'vegetables_emissions': emission_data.vegetables_emissions,
        'r134a_emissions': emission_data.r134a_emissions,
        'r410a_emissions': emission_data.r410a_emissions,
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
    food = emission_data.foodconsumption
    refrigerants = emission_data.refrigerants

    context = {
        'emission_data': emission_data,
        'energy': energy,
        'fuel': fuel,
        'transport': transport,
        'water': water,
        'waste': waste,
        'paper': paper,
        'food': food,               # Add this line
        'refrigerants': refrigerants  # Add this line
    }
    return render(request, 'emissions/emission_detail.html', context)

@login_required
def monthly_data_entry(request):
    current_year = datetime.now().year
    next_month = None
    
    # Check if user already has data for a different year
    existing_data_other_year = MonthlyEmissionData.objects.filter(
        user=request.user
    ).exclude(year=current_year).exists()
    
    if existing_data_other_year:
        return render(request, 'emissions/error.html', {
            'message': 'You already have emission data for another year. Only one year of data entry is allowed.'
        })

    if request.method == 'POST':
        year = int(request.POST.get('year'))
        if year != current_year:
            return render(request, 'emissions/error.html', {
                'message': f'Data entry is only allowed for the current year ({current_year})'
            })
        
        # Get or create the monthly data entry
        monthly_data, created = MonthlyEmissionData.objects.get_or_create(
            user=request.user,
            year=int(year),
            month=int(request.POST.get('month'))
        )
        
        # List all the fields we want to update
        fields = [
            'electricity_kwh', 'solar_generation_kwh', 'generator_fuel_liters',
            'diesel_liters', 'petrol_liters', 'lpg_kg',
            'distance_by_bus_km', 'distance_by_personal_km', 'distance_by_public_km', 'distance_by_ev_km',
            'water_consumed_kl', 'wastewater_treated_kl',
            'organic_waste_kg', 'plastic_waste_kg', 'sewage_liters', 'ewaste_kg',
            'paper_kg',
            # Add new fields
            'red_meat_kg', 'poultry_kg', 'vegetables_kg',
            'r134a_kg', 'r410a_kg'
        ]
        
        print("\nReceived values:")
        # Update each field and print values
        for field in fields:
            value = request.POST.get(field, '')
            print(f"{field}: {value}")
            if value == '':
                setattr(monthly_data, field, None)
            else:
                try:
                    float_value = float(value)
                    setattr(monthly_data, field, float_value)
                    print(f"Converted {field} to {float_value}")
                except ValueError:
                    print(f"Error converting {field}")
                    setattr(monthly_data, field, None)
        
        # Mark as complete if all fields have values
        monthly_data.is_complete = all(
            getattr(monthly_data, field) is not None 
            for field in fields
        )
        
        # Save and print final values
        monthly_data.save()
        print("\nSaved values in database:")
        for field in fields:
            print(f"{field}: {getattr(monthly_data, field)}")
        print(f"Record ID: {monthly_data.id}\n")
        
        return redirect('monthly_data_summary')
    
    # Get next empty month if we're continuing data entry
    if request.GET.get('next_month'):
        next_month = int(request.GET.get('next_month'))
    
    # Pre-fill form with existing data if available
    existing_data = None
    if request.GET.get('year') and request.GET.get('month'):
        year = int(request.GET.get('year'))
        month = int(request.GET.get('month'))
        
        if year != current_year:
            return render(request, 'emissions/error.html', {
                'message': f'Data entry is only allowed for the current year ({current_year})'
            })
        
        # Try to get existing data for this month
        existing_data = MonthlyEmissionData.objects.filter(
            user=request.user,
            year=year,
            month=month
        ).first()
        
        # If no existing data and prefill is requested, get last entered month's data
        if not existing_data and request.GET.get('prefill') == 'true':
            last_entry = MonthlyEmissionData.objects.filter(
                user=request.user,
                year=year,
                month__lt=month
            ).order_by('-month').first()
            
            if last_entry:
                existing_data = last_entry
                existing_data.pk = None  # Clear PK to treat as new entry
                existing_data.month = month  # Set correct month
    
    context = {
        'months': [
            (1, 'January'), (2, 'February'), (3, 'March'),
            (4, 'April'), (5, 'May'), (6, 'June'),
            (7, 'July'), (8, 'August'), (9, 'September'),
            (10, 'October'), (11, 'November'), (12, 'December')
        ],
        'years': [current_year],
        'existing_data': existing_data,
        'current_year': current_year,
        'is_prefilled': request.GET.get('prefill') == 'true',
        'next_month': next_month,
        'selected_month': next_month or (existing_data.month if existing_data else None)
    }
    return render(request, 'emissions/monthly_data_entry.html', context)

@login_required
def monthly_data_summary(request):
    year = request.GET.get('year', datetime.now().year)
    
    if request.method == 'POST' and request.POST.get('transfer_to_input') == '1':
        # Get all monthly data for the year
        monthly_data = MonthlyEmissionData.objects.filter(
            user=request.user,
            year=int(year)
        )
        
        # Calculate yearly totals
        yearly_totals = monthly_data.aggregate(
            electricity_kwh=Sum('electricity_kwh'),
            solar_generation_kwh=Sum('solar_generation_kwh'),
            generator_fuel_liters=Sum('generator_fuel_liters'),
            diesel_liters=Sum('diesel_liters'),
            petrol_liters=Sum('petrol_liters'),
            lpg_kg=Sum('lpg_kg'),
            distance_by_bus_km=Sum('distance_by_bus_km'),
            distance_by_personal_km=Sum('distance_by_personal_km'),
            distance_by_public_km=Sum('distance_by_public_km'),
            distance_by_ev_km=Sum('distance_by_ev_km'),
            water_consumed_kl=Sum('water_consumed_kl'),
            wastewater_treated_kl=Sum('wastewater_treated_kl'),
            organic_waste_kg=Sum('organic_waste_kg'),
            plastic_waste_kg=Sum('plastic_waste_kg'),
            sewage_liters=Sum('sewage_liters'),
            ewaste_kg=Sum('ewaste_kg'),
            paper_kg=Sum('paper_kg'),
            # Add new fields
            red_meat_kg=Sum('red_meat_kg'),
            poultry_kg=Sum('poultry_kg'),
            vegetables_kg=Sum('vegetables_kg'),
            r134a_kg=Sum('r134a_kg'),
            r410a_kg=Sum('r410a_kg')
        )
        
        # Redirect to input form with calculated totals
        params = {
            'year': year,
            **{k: v for k, v in yearly_totals.items() if v is not None}
        }
        return redirect(f'/emissions/input/?{urlencode(params)}')
    
    # Create a list of all months
    all_months = range(1, 13)
    months_data = {month: None for month in all_months}
    
    # Get existing data
    monthly_data = MonthlyEmissionData.objects.filter(
        user=request.user,
        year=int(year)
    ).order_by('month')
    
    # Fill in existing data
    for data in monthly_data:
        months_data[data.month] = data
    
    # Check if at least one month has all fields filled
    any_month_complete = False
    for data in monthly_data:
        fields_to_check = [
            'electricity_kwh', 'solar_generation_kwh', 'generator_fuel_liters',
            'diesel_liters', 'petrol_liters', 'lpg_kg',
            'distance_by_bus_km', 'distance_by_personal_km', 'distance_by_public_km', 'distance_by_ev_km',
            'water_consumed_kl', 'wastewater_treated_kl',
            'organic_waste_kg', 'plastic_waste_kg', 'sewage_liters', 'ewaste_kg',
            'paper_kg'
        ]
        if all(getattr(data, field) is not None for field in fields_to_check):
            any_month_complete = True
            break
    
    # Calculate totals only from existing data
    totals = monthly_data.aggregate(
        total_electricity=Sum('electricity_kwh'),
        total_solar=Sum('solar_generation_kwh'),
        total_generator=Sum('generator_fuel_liters'),
        total_diesel=Sum('diesel_liters'),
        total_petrol=Sum('petrol_liters'),
        total_lpg=Sum('lpg_kg'),
        total_bus=Sum('distance_by_bus_km'),
        total_personal=Sum('distance_by_personal_km'),
        total_public=Sum('distance_by_public_km'),
        total_ev=Sum('distance_by_ev_km'),
        total_water=Sum('water_consumed_kl'),
        total_wastewater=Sum('wastewater_treated_kl'),
        total_organic=Sum('organic_waste_kg'),
        total_plastic=Sum('plastic_waste_kg'),
        total_sewage=Sum('sewage_liters'),
        total_ewaste=Sum('ewaste_kg'),
        total_paper=Sum('paper_kg'),
        total_red_meat=Sum('red_meat_kg'),
        total_poultry=Sum('poultry_kg'),
        total_vegetables=Sum('vegetables_kg'),
        total_r134a=Sum('r134a_kg'),
        total_r410a=Sum('r410a_kg')
    )
    
    # Get all available years
    available_years = MonthlyEmissionData.objects.filter(
        user=request.user
    ).values_list('year', flat=True).distinct().order_by('year')
    
    # Create month labels
    month_labels = [
        (1, 'January'), (2, 'February'), (3, 'March'),
        (4, 'April'), (5, 'May'), (6, 'June'),
        (7, 'July'), (8, 'August'), (9, 'September'),
        (10, 'October'), (11, 'November'), (12, 'December')
    ]
    
    # Find next empty month
    next_month = None
    for month in all_months:
        if month not in [d.month for d in monthly_data]:
            next_month = month
            break
    
    # Check if all totals are non-empty
    all_totals_present = all(
        value is not None and value != 0 
        for value in totals.values()
    )
    
    months_complete = monthly_data.count() == 12 and all_totals_present
    
    context = {
        'monthly_data': [
            {
                'month_num': month,
                'month_name': dict(month_labels)[month],
                'data': months_data[month]
            } 
            for month in all_months
        ],
        'totals': totals,
        'months_complete': any_month_complete,  # Changed condition
        'year': year,
        'available_years': available_years,
        'next_month': next_month,
    }
    
    return render(request, 'emissions/monthly_data_summary.html', context)

def downloadSampleCSV():
    sampleData = [
        ["year", "electricity_kwh", "solar_generation_kwh", "generator_fuel_liters", 
         "diesel_liters", "petrol_liters", "lpg_kg", "distance_by_bus_km", 
         "distance_by_personal_km", "distance_by_public_km", "distance_by_ev_km", 
         "water_consumed_kl", "wastewater_treated_kl", "organic_waste_kg", 
         "plastic_waste_kg", "sewage_liters", "ewaste_kg", "paper_kg",
         "red_meat_kg", "poultry_kg", "vegetables_kg", "r134a_kg", "r410a_kg"],
        ["2023", "1000", "200", "50", "300", "400", "100", "500", "600", 
         "700", "800", "900", "1000", "1100", "1200", "1300", "1400", 
         "1500", "100", "200", "300", "10", "15"]
    ]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_data.csv"'
    writer = csv.writer(response)
    for row in sampleData:
        writer.writerow(row)
    return response
