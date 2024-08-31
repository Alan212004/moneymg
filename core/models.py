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
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    DEBIT = 'D'
    CREDIT = 'C'
    
    TRANSACTION_TYPE_CHOICES = [
        (DEBIT, 'Debit'),
        (CREDIT, 'Credit'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount}"

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone = PhoneNumberField(max_length=12,null=True, blank=True, validators=[MinLengthValidator(10)])
    address = models.TextField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True) 

    def __str__(self):
        return self.name