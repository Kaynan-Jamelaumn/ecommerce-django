from django.db import models

from product.models import ProductVariation

from account.models import Address
from django.conf import settings  # Here


# Create your models here.
class Order(models.Model):

    variation = models.ForeignKey(ProductVariation,
                                  on_delete=models.DO_NOTHING)
    created_at = models.DateField(auto_now_add=True)
    uploaded_at = models.DateField(auto_now=True)
    quantity = models.IntegerField()
    total = models.FloatField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Orders(models.Model):
    STATUS_CHOICES = (('C', 'CREATED'), ('P', 'PAID_TO_DELIEVER'),('D', 'DELIVERED'))

    order = models.ManyToManyField(Order)
    created_at = models.DateField(auto_now_add=True)
    uploaded_at = models.DateField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    address = models.ForeignKey(Address,
                                on_delete=models.DO_NOTHING,
                                blank=False,
                                null=False)
    status = models.CharField(max_length=1,
                              choices=STATUS_CHOICES,
                              blank=False,
                              null=False)
    total_paid = models.FloatField()