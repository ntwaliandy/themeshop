from django.db import models

# Create your models here.

class UserDetails(models.Model):
    full_name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=15, null=False, blank=False, unique=True)
    country = models.CharField(max_length=30, null=False, blank=False)
    postcode = models.CharField(max_length=200, null=False, blank=False)
    user = models.CharField(max_length=2000, null=False, blank=False)

    def __str__(self):
        return self.full_name + '  country: ' + self.country