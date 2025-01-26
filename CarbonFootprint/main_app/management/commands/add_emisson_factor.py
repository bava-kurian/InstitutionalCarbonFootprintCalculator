from django.core.management.base import BaseCommand
from main_app.models import EmissionFactor

class Command(BaseCommand):
    help = 'Add default emission factors'

    def handle(self, *args, **kwargs):
        emission_factors = [
            {'category': 'energy', 'factor': 0.5},
            {'category': 'transportation', 'factor': 0.3},
            {'category': 'water', 'factor': 0.2},
            {'category': 'waste', 'factor': 0.4},
        ]

        for ef in emission_factors:
            EmissionFactor.objects.update_or_create(category=ef['category'], defaults={'factor': ef['factor']})

        self.stdout.write(self.style.SUCCESS('Successfully added emission factors'))