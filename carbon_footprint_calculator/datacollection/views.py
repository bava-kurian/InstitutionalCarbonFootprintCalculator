from django.shortcuts import render, redirect
from .forms import (
    ElectricityForm, SolarGenerationForm, GeneratorFuelForm, DieselForm, PetrolForm, LPGForm,
    BusDistanceForm, PersonalDistanceForm, PublicDistanceForm, EVDistanceForm, WaterConsumedForm,
    WastewaterTreatedForm, OrganicWasteForm, PlasticWasteForm, SewageForm, EWasteForm, PaperForm
)

def collect_data(request):
    if request.method == 'POST':
        forms = [
            ElectricityForm(request.POST, prefix='electricity'),
            SolarGenerationForm(request.POST, prefix='solar'),
            GeneratorFuelForm(request.POST, prefix='generator'),
            DieselForm(request.POST, prefix='diesel'),
            PetrolForm(request.POST, prefix='petrol'),
            LPGForm(request.POST, prefix='lpg'),
            BusDistanceForm(request.POST, prefix='bus'),
            PersonalDistanceForm(request.POST, prefix='personal'),
            PublicDistanceForm(request.POST, prefix='public'),
            EVDistanceForm(request.POST, prefix='ev'),
            WaterConsumedForm(request.POST, prefix='water'),
            WastewaterTreatedForm(request.POST, prefix='wastewater'),
            OrganicWasteForm(request.POST, prefix='organic'),
            PlasticWasteForm(request.POST, prefix='plastic'),
            SewageForm(request.POST, prefix='sewage'),
            EWasteForm(request.POST, prefix='ewaste'),
            PaperForm(request.POST, prefix='paper')
        ]
        if all(form.is_valid() for form in forms):
            for form in forms:
                form.save()
            return redirect('data_collection_success')
    else:
        forms = [
            ElectricityForm(prefix='electricity'),
            SolarGenerationForm(prefix='solar'),
            GeneratorFuelForm(prefix='generator'),
            DieselForm(prefix='diesel'),
            PetrolForm(prefix='petrol'),
            LPGForm(prefix='lpg'),
            BusDistanceForm(prefix='bus'),
            PersonalDistanceForm(prefix='personal'),
            PublicDistanceForm(prefix='public'),
            EVDistanceForm(prefix='ev'),
            WaterConsumedForm(prefix='water'),
            WastewaterTreatedForm(prefix='wastewater'),
            OrganicWasteForm(prefix='organic'),
            PlasticWasteForm(prefix='plastic'),
            SewageForm(prefix='sewage'),
            EWasteForm(prefix='ewaste'),
            PaperForm(prefix='paper')
        ]
    return render(request, 'datacollection/collect_data.html', {'forms': forms})

def data_collection_success(request):
    return render(request, 'datacollection/success.html')
