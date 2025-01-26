from django.db import models
from django.contrib.auth.models import User

class Institution(models.Model):
    INSTITUTION_TYPE_CHOICES = [
        ('Educational', 'Educational'),
        ('Business', 'Business'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=INSTITUTION_TYPE_CHOICES)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name