from django.db import models
from django.utils import timezone

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, null=True)
    address = models.TextField(max_length=100,blank=True, null=True)
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
    contact_info = models.TextField()

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    def total_value(self):
        return self.quantity * self.unit_price

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('I', 'Inbound'),
        ('O', 'Outbound'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField()
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.quantity} of {self.product.name}"