from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from xhtml2pdf import pisa
from .models import EmissionData

@login_required
def render_pdf_view(request, emi_data_id):
    emission_data = get_object_or_404(EmissionData, pk=emi_data_id, user=request.user)
    template_path = 'emissions/pdf_template.html'
    context = {
        'emission_data': emission_data,
        'electricity_emissions': emission_data.electricity_emissions,
        'diesel_emissions': emission_data.diesel_emissions,
        'petrol_emissions': emission_data.petrol_emissions,
        'lpg_emissions': emission_data.lpg_emissions,
        'public_transport_emissions': emission_data.public_transport_emissions,
        'water_supply_emissions': emission_data.water_supply_emissions,
        'plastic_waste_emissions': emission_data.plastic_waste_emissions,
        'total_emissions': emission_data.total_emissions,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="emission_report_{emi_data_id}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
