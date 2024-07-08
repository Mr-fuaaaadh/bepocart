from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from bepocartAdmin.models import *
from django.utils import timezone
import uuid

current_time = timezone.now()

class Customer(models.Model):
    first_name = models.CharField(max_length=100,null=True, blank=False)
    last_name = models.CharField(max_length=100,null=True, blank=False)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)
    image = models.ImageField(max_length=100, upload_to='UserProfile',null=True)
    place = models.CharField(max_length=100, null=True,blank=False)
    zip_code = models.CharField(max_length=6,null=True,blank=False)
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
    coupon_type = models.CharField(max_length=20, default='Percentage')
    discount = models.DecimalField(max_digits=10, decimal_places=2) 
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, default='In Active')  
    max_uses = models.IntegerField(default=1) 
    used_count = models.IntegerField(default=0)
    discount_product = models.ManyToManyField('bepocartAdmin.Product', blank=True)
    discount_category = models.ManyToManyField('bepocartAdmin.Subcategory', blank=True)

    def __str__(self):
        return self.code

    def is_valid(self):
        return (
            self.status == 'Active' and
            self.used_count < self.max_uses and
            self.start_date <= timezone.now().date() <= self.end_date
        )
    
    class Meta:
        db_table = "Coupon"

    def apply_coupon(self, order_total, products=None):
        if not self.is_valid():
            return order_total, False

        if self.discount_product.exists() and (not products or not any(p in self.discount_product.all() for p in products)):
            return order_total, False

        if self.discount_category.exists() and (not products or not any(p.category in self.discount_category.all() for p in products)):
            return order_total, False

        if self.coupon_type.lower() == 'percentage':
            discount_amount = (self.discount / 100) * order_total
        else:
            discount_amount = self.discount

        new_total = max(order_total - discount_amount, 0)
        self.used_count += 1  
        self.save()  
        return new_total, True
    
class Order(models.Model):
    order_id = models.CharField(max_length=20, null=True, unique=True, editable=False)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    created_time = models.TimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    coupon = models.ForeignKey('Coupon', on_delete=models.CASCADE, null=True)
    payment_method = models.CharField(max_length=20, null=True)
    payment_id = models.CharField(max_length=100, null=True)
    
    def save(self, *args, **kwargs):
        if not self.created_time:
            self.created_time = timezone.now().time()
        
        if not self.order_id:
            self.order_id = self.generate_order_id()
        
        super().save(*args, **kwargs)
        self.calculate_total()

    def generate_order_id(self):
        date_str = timezone.now().strftime('%Y%m%d')
        unique_id = uuid.uuid4().hex[:6].upper()  # Generate a random unique identifier
        return f'{date_str}-{unique_id}'

    def calculate_total(self):
        total = sum(item.price * item.quantity for item in self.order_items.all())
        discount_value = 0
        
        if self.coupon:
            if self.coupon.coupon_type == 'Percentage':
                applicable_items = self.order_items.filter(product__category=self.coupon.discount_category)
                discount_value = sum(item.product.salePrice * item.quantity for item in applicable_items) * (self.coupon.discount / 100)
            elif self.coupon.coupon_type == 'Fixed Amount':
                discount_value = self.coupon.discount

            total -= min(discount_value, total)
            print(f"Discount applied: {discount_value}, Total after discount: {total}")  

        self.total_amount = total

        if self.payment_method == 'COD':
            self.total_amount += 40
        
        super().save(update_fields=['total_amount'])  # Save the order after calculating total
        print(f"Final total amount saved: {self.total_amount}")

    def __str__(self):
        return self.order_id




class OrderItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey('bepocartAdmin.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=False)
    color = models.CharField(max_length=20,null=True)
    size = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.price * self.quantity