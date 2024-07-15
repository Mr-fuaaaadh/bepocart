from django.db import models
from django.utils import timezone
from bepocartBackend.models import Customer, Order, OrderItem, Coupon
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
    slug = models.SlugField(max_length=250,unique=True,null=True)
    image = models.ImageField(max_length=100, upload_to="Subcategory/", null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Subcategory'
    


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250,unique=True,null=True)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    salePrice = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    category = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], default=0   )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]


class Offer(models.Model):
    # TITLE
    name = models.CharField(max_length=255)

    buy = models.CharField(max_length=100) # select BUY OR SPEND

    amount = models.IntegerField(null=True) # select BUY OR SPEND

    get = models.CharField(max_length=100) # selectef option is BUY   get option

    get_value = models.IntegerField(null=True) # free quantity

    method = models.CharField(max_length=100) # selecte FREE OR 0 OFF

    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True) # IF METHOD SELECT %OFF    ADD PERSONTAGE 

    
    offer_products = models.ManyToManyField(Product, related_name='offers', blank=True) # OFFER APPROVED PRODUCTS
    exclude_products = models.ManyToManyField(Product, related_name='exclude_products', blank=True) # NOT OFFER APPROVED PRODUCTS

    # OR

    offer_category = models.ManyToManyField(Subcategory, related_name='offers', blank=True)  # OFFER APPROVED CATEGORIES
    excluded_offer_category = models.ManyToManyField(Subcategory, related_name='exclude_categories', blank=True) # OFFER NOT APPROVED CATEGORIES

    # OFFER START DATE AND END DATE
    start_date = models.DateField()
    end_date = models.DateField()

    # OFFER NOT APPROVED COUPONS
    not_allowed_coupons = models.ManyToManyField(Coupon,blank=True)
    messages = models.CharField(max_length=500, null=True)
    coupon_user_limit = models.IntegerField(null=True)
    coupon_use_order_limit = models.IntegerField(null=True)
    shipping_charge = models.IntegerField(default=0)
    

    #dISCOUNTED APPROVED PRODUCTS AND CATEGORY
    is_active = models.CharField(max_length=200, default="Allowd",null=True)
    discount_approved_products = models.ManyToManyField(Product,null=True,blank=True , related_name='discount_approved_products')
    discount_not_allowd_products = models.ManyToManyField(Product,null=True,blank=True , related_name='discount_not_allowd_products')
    discount_approved_category = models.ManyToManyField(Category,null=True,blank=True , related_name='discount_approved_category')
    discount_not_allowd_category = models.ManyToManyField(Category,null=True,blank=True , related_name='discount_not_allowd_category')





    def __str__(self):
        return self.name

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date


    def applies_to_product(self, product):
        return self.products.filter(pk=product.pk).exists()

    def applies_to_category(self, category):
        return self.categories.filter(pk=category.pk).exists()



class ProducyImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    color = models.CharField(max_length=100,null=True)
    image1 = models.ImageField(max_length=100, upload_to='product/Images')
    image2 = models.ImageField(max_length=100, upload_to='product/Images')
    image3 = models.ImageField(max_length=100, upload_to='product/Images')
    image4 = models.ImageField(max_length=100, upload_to='product/Images')
    image5 = models.ImageField(max_length=100, upload_to='product/Images')

    class Meta :
        db_table = 'ProductImage'

class Productverient(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank=False)
    color = models.ForeignKey(ProducyImage, on_delete=models.CASCADE, related_name='verients')
    size = models.CharField(max_length=100,null=True)
    stock = models.PositiveIntegerField(default=0)

    class Meta :
        db_table = 'Productverient'


class Wishlist(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta :
        db_table ="Whishlist"


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product =  models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    color = models.CharField(max_length=100,null=True)
    size = models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta :
        db_table = "Cart"


class Blog(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(max_length=100, upload_to="blog")
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.CharField(default="Active", null=True)

    def publish(self):
        self.published_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
    class Meta :
        db_table = "Blog"




class Coin(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    source = models.CharField(max_length=100) 
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.amount} coins from {self.source}"
    
from django.core.exceptions import ValidationError

class CoinValue(models.Model):
    coin = models.IntegerField()
    value = models.FloatField()
    login_value = models.IntegerField(default=10,null=True)
    first_payment_value = models.IntegerField(default=100,null=True)
    payment_value = models.FloatField(null=True) 
    referral_point = models.IntegerField(default=10,null=True)
    review_reward = models.IntegerField(default=10,null=True)
    birthday_reward = models.IntegerField(default=10,null=True)
    anniversary_reward = models.IntegerField(default=10,null=True)
    timestamp = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.coin} - {self.value}"

    def clean(self):
        if CoinValue.objects.exists() and not self.pk:
            raise ValidationError("Only one instance of CoinValue is allowed.")
        if not (0 <= self.payment_value <= 100):
            raise ValidationError("Payment value must be a percentage between 0 and 100.")
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)