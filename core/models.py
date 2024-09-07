from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinLengthValidator
from django.utils import timezone
from django.contrib.auth.models import User

class Customer(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    
    GENDER = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    nick_name = models.CharField(max_length=100, blank=True, null=True)
    phone = PhoneNumberField(max_length=15, null=True, region="IN", default="+91 ", validators=[MinLengthValidator(10)])
    gender = models.CharField(max_length=6, null=True, choices=GENDER)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(max_length=100, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        user_info = self.user.username if self.user else 'Unknown User'
        return f"Customer -> {self.name}"


class Supplier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    phone = PhoneNumberField(max_length=15, null=True, blank=True,region="IN", default="+91 ", validators=[MinLengthValidator(10)])
    address = models.TextField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True) 
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        user_info = self.user.username if self.user else 'Unknown User'
        return f"Supplier -> {self.name}"

class STransaction(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('mixed', 'Cash and Bank Mixed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_type = models.CharField(max_length=5, choices=PAYMENT_TYPE_CHOICES, blank=True)
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer.name} - {self.total_amount}"

class PTransaction(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('mixed', 'Cash and Bank Mixed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_type = models.CharField(max_length=5, choices=PAYMENT_TYPE_CHOICES, blank=True)
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.supplier.name} - {self.total_amount}"
