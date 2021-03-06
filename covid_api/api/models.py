from django.db import models
from django_countries.fields import CountryField

# Create your models here.
class UserProfile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=20)
    country = CountryField(null=True)

    def __str__(self):
        return self.first_name + self.last_name