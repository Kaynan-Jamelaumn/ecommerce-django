from django.contrib import admin

# Register your models here.
from . import models

class VariationInLine(admin.TabularInline):
    model = models.ProductVariation
    extra = 1
  
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',
                    'category', 'subcategory', 'on_promotion',)

    list_editable = ('on_promotion', )
    inlines = [ VariationInLine, ]

class VariationAdmin(admin.ModelAdmin):
    list_display = ('name', 'product',)


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.SubCategory, SubCategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductVariation, VariationAdmin)
admin.site.register(models.ExtraProductPicture)
admin.site.register(models.ExtraVariationProductPicture)