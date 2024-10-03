from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinLengthValidator
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.exceptions import ValidationError

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
    balance = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        user_info = self.user.username if self.user else 'Unknown User'
        return f"Customer -> {self.name}"
    

class Product(models.Model):
    TYPE_CHOICES = [
        ('box', 'Box'),
        ('number', 'Number'),
        ('litre', 'Litre'),
        ('pack', 'Pack'),
        ('kg', 'Kilogram'),
        ('gram', 'Gram'),
    ]
    
    TAX = [
    (0.00, '0%'),
    (5.00, '5%'),
    (12.00, '12%'),
    (18.00, '18%'),
    (28.00, '28%'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/product_images/', default='images/product_images/default_product.png', blank=True)
    name = models.CharField(max_length=255)
    print_name = models.CharField(max_length=255, blank=True)
    hsn_code = models.CharField(max_length=20, blank=True)
    category = models.CharField(max_length=100)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    purchase_quantity = models.PositiveIntegerField(default=0, blank=True)  # Initially set to 0
    purchase_type = models.CharField(max_length=50, choices=TYPE_CHOICES)

    sales_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    sales_quantity = models.PositiveIntegerField(default=0, blank=True)  # Initially set to 0
    sales_type = models.CharField(max_length=50, choices=TYPE_CHOICES)

    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True, choices=TAX)
    expiry_date = models.DateField(null=True, blank=True)
    purchase_date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='available' , choices=[('available', 'Available'), ('out_of_stock', 'Out of Stock')])

    def save(self, *args, **kwargs):
        # Set purchase_quantity to sales_quantity if it is not explicitly set
        if self.purchase_quantity == 0:
            self.purchase_quantity = self.sales_quantity

        # Validate that sales_price does not exceed mrp
        if self.sales_price > self.mrp:
            raise ValidationError("Sales price cannot exceed MRP.")

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    
class BalanceHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date']

def create_balance_history(customer, amount, paid, balance, description):
    BalanceHistory.objects.create(
        customer=customer,
        amount=amount,
        paid=paid,
        balance=balance,
        description=description
    )

class Supplier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    phone = PhoneNumberField(max_length=15, null=True, blank=True,region="IN", default="+91 ", validators=[MinLengthValidator(10)])
    address = models.TextField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True) 
    balance = models.DecimalField(max_digits=50, decimal_places=2, default=0)
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
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # New discount field
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

######################################################


   