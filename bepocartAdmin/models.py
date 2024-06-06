from django.db import models
from django.utils import timezone
from bepocartBackend.models import *
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.hashers import make_password

class Carousal(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="banner", max_length=100)


    class Meta :
        db_table="banner"


class OfferBanner(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="offer_banner", max_length=100)

    class Meta :
        db_table = "Offer_Banner"


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category/",max_length=100, null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'






class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(max_length=100, upload_to="Subcategory/", null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Subcategory'
    



class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    salePrice = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    stock = models.IntegerField()
    category = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], default=0   )
    offer_banner = models.ForeignKey(OfferBanner, on_delete=models.CASCADE, null=True)
    offer_type = models.CharField(max_length=100, null=True)
    offer_start_date = models.DateTimeField(blank=True, null=True)
    offer_end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]



class Wishlist(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta :
        db_table ="Whishlist"


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product =  models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta :
        db_table = "Cart"





    