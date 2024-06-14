from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from bepocartAdmin.models import *
class Customer(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)
    image = models.ImageField(max_length=100, upload_to='UserProfile',null=True)
    password = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.pk or 'password' in kwargs:  
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    class Meta:
        db_table = "customer"



class Address(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address =  models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    phone = models.CharField(max_length=10)
    pincode = models.IntegerField()
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    note = models.TextField(max_length=250)


    class Meta :
        db_table = "Address"



class OTP(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)

    class Meta :
        db_table = "OTP"







class RecentlyViewedProduct(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey('bepocartAdmin.Product', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-viewed_at']




class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    coupon_type = models.CharField(max_length=20,default='Percentage')
    discount = models.DecimalField(max_digits=10, decimal_places=2) 
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(default='In Active')  # True if the coupon is active
    max_uses = models.IntegerField(default=1)  # Number of times the coupon can be used
    used_count = models.IntegerField(default=0)  # Number of times the coupon has been used
    discount_product = models.ForeignKey('bepocartAdmin.Product', null=True, blank=True, on_delete=models.SET_NULL)
    discount_category = models.ForeignKey('bepocartAdmin.Subcategory', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.code

    def is_valid(self):
        return (
            self.status and
            self.used_count < self.max_uses and
            self.start_date <= timezone.now() <= self.end_date
        )
    
    class Meta :
        db_table ="Coupen"

    def apply_coupon(self, order_total, products=None):
        if not self.is_valid():
            return order_total, False

        if self.discount_product and (not products or self.discount_product not in products):
            return order_total, False

        if self.discount_category and (not products or not any(p.category == self.discount_category for p in products)):
            return order_total, False

        if self.coupon_type == 'percentage':
            discount_amount = (self.discount / 100) * order_total
        else:
            discount_amount = self.discount

        new_total = max(order_total - discount_amount, 0)
        self.used_count += 1
        self.save()
        return new_total, True
    
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE, null=True)
    payment_method = models.CharField(max_length=20,null=True)

    def calculate_total(self):
        from bepocartAdmin.models import Product
        self.total_amount = sum(item.total_amount() for item in self.order_items.all())
        self.save()

class OrderItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey('bepocartAdmin.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.price * self.quantity