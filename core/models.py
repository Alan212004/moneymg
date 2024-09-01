from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinLengthValidator
from django.utils import timezone

class Customer(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    
    GENDER = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]
    
    name = models.CharField(max_length=100, null=True)
    nick_name = models.CharField(max_length=100, blank=True, null=True)
    phone = PhoneNumberField(max_length=15, null=True, validators=[MinLengthValidator(10)])
    gender = models.CharField(max_length=6, null=True, choices=GENDER)
    email = models.EmailField(unique=True, blank=True, null=True)
    address = models.TextField(max_length=100, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone = PhoneNumberField(max_length=15, null=True, blank=True, validators=[MinLengthValidator(10)])
    address = models.TextField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True) 
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class STransaction(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('mixed', 'Cash and Bank Mixed'),
    ]

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

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_type = models.CharField(max_length=5, choices=PAYMENT_TYPE_CHOICES, blank=True)
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.supplier.name} - {self.total_amount}"
