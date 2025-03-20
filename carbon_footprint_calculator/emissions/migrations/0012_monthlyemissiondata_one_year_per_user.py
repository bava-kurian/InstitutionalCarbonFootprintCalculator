# Generated by Django 5.1.6 on 2025-03-09 08:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emissions', '0011_alter_monthlyemissiondata_diesel_liters_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='monthlyemissiondata',
            constraint=models.UniqueConstraint(condition=models.Q(('year__lt', models.F('year'))), fields=('user',), name='one_year_per_user'),
        ),
    ]
