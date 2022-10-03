from django.db import models

# Create your models here. # Here
from django.conf import settings # Here



class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    number = models.IntegerField()
    state = models.CharField(max_length=255)
    post_code    = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
                            # Here