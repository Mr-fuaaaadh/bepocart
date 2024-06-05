from django.db import models
from django.contrib.auth.hashers import make_password, check_password
class Customer(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.pk or 'password' in kwargs:  # Hash the password only if it's being created or updated
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    class Meta:
        db_table = "customer"




