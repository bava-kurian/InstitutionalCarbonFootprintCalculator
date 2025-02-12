from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)

class Institution(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    institution_type = models.CharField(max_length=50, choices=[('Educational', 'Educational'), ('Business', 'Business'), ('Other', 'Other')])
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)