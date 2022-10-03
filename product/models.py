from django.db import models
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255, unique=False, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("product:category", kwargs={"category_id": self.id})


class SubCategory(models.Model):
    name = models.CharField(max_length=255, unique=False, blank=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("product:subcategory",
                       kwargs={
                           "category_id": self.category.id,
                           "subcategory_id": self.id
                       })


class Product(models.Model):
    name = models.CharField(max_length=255, unique=False, blank=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 unique=False)
    subcategory = models.ForeignKey(SubCategory,
                                    on_delete=models.CASCADE,
                                    unique=False,
                                    blank=True,
                                    null=True)
    #short_description = models.CharField(max_length=255, unique=False, blank=True, null=True)
    #long_description = models.TextField(unique=False, blank=True, null=False)
    image = models.ImageField(blank=True,
                              null=True,
                              unique=False,
                              upload_to='product_images/%Y/%m/%d')
    on_promotion = models.BooleanField(default=False)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("product:detail", kwargs={"slug": self.slug})


class ProductVariation(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                unique=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField()
    promotion_price = models.FloatField(blank=True, default=None)
    stock = models.IntegerField()
    short_description = models.CharField(max_length=255,
                                         unique=False,
                                         blank=True,
                                         null=False)
    long_description = models.TextField(unique=False, blank=True, null=False)
    image = models.ImageField(blank=True,
                              null=True,
                              unique=False,
                              upload_to='product_images/%Y/%m/%d')
    created_at = models.DateField(auto_now_add=True)
    uploaded_at = models.DateField(auto_now=True)
    on_promotion = models.BooleanField(default=False)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product:hate", kwargs={"product_id": self.id})


class ExtraProductPicture(models.Model):
    image = models.ImageField(blank=True,
                              null=True,
                              unique=False,
                              upload_to='product_images/%Y/%m/%d')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    uploaded_at = models.DateField(auto_now=True)

   # def __str__(self):
    #    return self.product


class ExtraVariationProductPicture(models.Model):
    image = models.ImageField(blank=True,
                              null=True,
                              unique=False,
                              upload_to='product_images/%Y/%m/%d')
    variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    uploaded_at = models.DateField(auto_now=True)

    #def __str__(self):
      #  return self.variation
