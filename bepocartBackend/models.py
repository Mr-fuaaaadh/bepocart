from django.db import models
from django.contrib.auth.hashers import make_password, check_password
class Customer(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)
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




class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def calculate_total(self):
        from bepocartAdmin.models import Product
        self.total_amount = sum(item.total_price() for item in self.order_items.all())
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey('bepocartAdmin.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.price * self.quantity