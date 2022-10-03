from django.contrib import admin

# Register your models here.
from .models import Order, Orders
"""
from product.models import ProductVariation


class ProductInLine(admin.TabularInline):
    model = ProductVariation
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductVariation,
    ]


admin.site.register(Order, OrderAdmin)
"""
admin.site.register(Order)
admin.site.register(Orders)